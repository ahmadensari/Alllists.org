"""Taxonomy loaders (plan P1.07): Overture, Foursquare, ISCO-08 and our own CSV, from local files.

Each loader makes concepts with a crosswalk row naming the outside code, so a source record's category finds our list
type. Licences differ: confirm the licence of each downloaded file before loading it (plan section 7.1)."""

import csv
import io
import re

from django.db import transaction
from django.utils.text import slugify

from core.textfold import fold

from .models import Concept, ConceptCrosswalk, ConceptLabel
from .services import TaxonomyError, create_concept


def _slug(text, taken_kind):
    base = slugify(text)[:100] or "concept"
    slug, n = base, 2
    while Concept.objects.filter(kind=taken_kind, slug=slug).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


def _promote(concept):
    from .models import ListTypeSettings, ReservedSlug

    concept.kind = Concept.Kind.LIST_TYPE
    concept.save(update_fields=["kind"])
    ReservedSlug.objects.get_or_create(slug=concept.slug, kind="list_type")
    ListTypeSettings.objects.get_or_create(concept=concept)


def _get_or_make(kind, system, code, name, parent, language="en"):
    cw = ConceptCrosswalk.objects.filter(system=system, code=code).select_related("concept").first()
    if cw:
        c = cw.concept
        if kind == Concept.Kind.LIST_TYPE and c.kind == Concept.Kind.FAMILY:
            _promote(c)  # first seen only as somebody's parent, now also a list type in its own right
        return c, False
    try:
        c = create_concept(kind=kind, name=name, language=language, slug=_slug(name, kind), parent=parent)
    except TaxonomyError:
        c = create_concept(kind=kind, name=name, language=language, slug=_slug(name + " list", kind), parent=parent)
    ConceptCrosswalk.objects.create(concept=c, system=system, code=code, match_type="exact")
    return c, True


def _add_label(concept, language, text, kind="synonym"):
    t = fold(text)
    if text and not concept.labels.filter(language=language, text_fold=t).exists():
        ConceptLabel.objects.create(concept=concept, language=language, kind=kind, text=text, text_fold=t)


@transaction.atomic
def load_overture_categories(text, *, kind=Concept.Kind.LIST_TYPE):
    """Overture category list: lines like `gas_station;[energy_and_utilities,gas_station]` or `code,"[a,b,c]"`.
    The last element is the category, earlier ones its ancestors. Returns {"created": n, "existing": n}."""
    made = seen = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("category_code"):
            continue
        m = re.match(r'^"?([\w.]+)"?\s*[;,\t]\s*"?\[(.*?)\]"?\s*$', line)
        if not m:
            continue
        chain = [c.strip() for c in m.group(2).split(",") if c.strip()]
        parent = None
        for i, code in enumerate(chain):
            concept, new = _get_or_make(
                Concept.Kind.FAMILY if i < len(chain) - 1 and kind == Concept.Kind.LIST_TYPE else kind,
                "overture",
                code,
                code.replace("_", " ").capitalize(),
                parent,
            )
            made, seen = made + new, seen + (not new)
            parent = concept
    return {"created": made, "existing": seen}


@transaction.atomic
def load_foursquare_categories(text, *, kind=Concept.Kind.LIST_TYPE):
    """Foursquare open taxonomy as TSV/CSV with `category_id` and `category_label` (`A > B > C`)."""
    dialect = csv.excel_tab if "\t" in text.splitlines()[0] else csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    made = seen = 0
    for row in reader:
        label = (row.get("category_label") or "").strip()
        code = (row.get("category_id") or row.get("fsq_category_id") or "").strip()
        if not label or not code:
            continue
        names = [n.strip() for n in label.split(">")]
        parent = None
        for i, name in enumerate(names):
            last = i == len(names) - 1
            kd = kind if last else Concept.Kind.FAMILY
            pkey = "path:" + " > ".join(
                names[: i + 1]
            )  # the same node seen as a leaf in one row and an ancestor in another
            concept, new = _get_or_make(kd, "foursquare", pkey, name, parent)
            if last and not ConceptCrosswalk.objects.filter(system="foursquare", code=code).exists():
                ConceptCrosswalk.objects.create(concept=concept, system="foursquare", code=code, match_type="exact")
            made, seen = made + new, seen + (not new)
            parent = concept
    return {"created": made, "existing": seen}


@transaction.atomic
def load_isco(text):
    """ISCO-08 occupations (`code,title`) as speciality concepts for people-based lists. Groups by code prefix."""
    made = seen = 0
    for row in csv.reader(io.StringIO(text)):
        if len(row) < 2 or not row[0].strip().isdigit():
            continue
        code, title = row[0].strip(), row[1].strip()
        parent = None
        if len(code) > 1:
            cw = ConceptCrosswalk.objects.filter(system="isco", code=code[:-1], concept__kind="speciality").first()
            parent = cw.concept if cw else None
        _, new = _get_or_make(Concept.Kind.SPECIALITY, "isco", code, title, parent)
        made, seen = made + new, seen + (not new)
    return {"created": made, "existing": seen}


@transaction.atomic
def load_own_csv(text):
    """Our own layer: columns `kind,slug,name,language,parent_slug,synonyms` (synonyms separated by `|`; a synonym may
    be written `text@lang`). Existing slugs gain labels; nothing is renamed or removed."""
    made = seen = 0
    for row in csv.DictReader(io.StringIO(text)):
        kind, slug = (row.get("kind") or "").strip(), (row.get("slug") or "").strip()
        if not (kind and slug and row.get("name")):
            continue
        concept = Concept.objects.filter(kind=kind, slug=slug).first()
        if concept is None:
            parent = Concept.objects.filter(kind=kind, slug=(row.get("parent_slug") or "").strip()).first()
            concept = create_concept(
                kind=kind, name=row["name"], language=row.get("language") or "en", slug=slug, parent=parent
            )
            made += 1
        else:
            seen += 1
        for syn in filter(None, (row.get("synonyms") or "").split("|")):
            text_, _, lang = syn.partition("@")
            _add_label(concept, lang or row.get("language") or "en", text_.strip())
    return {"created": made, "existing": seen}


def concept_for_code(system, code):
    cw = ConceptCrosswalk.objects.filter(system=system, code=code).select_related("concept").first()
    return cw.concept if cw else None
