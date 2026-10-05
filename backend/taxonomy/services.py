from django.db import transaction
from django.utils.text import slugify

from core.models import RegistryVersion
from core.textfold import fold

from .models import AddonField, AddonTemplate, Concept, ConceptLabel, ListTypeSettings, ReservedSlug

SYSTEM_SLUGS = {"e", "search", "add", "claim", "wrong", "message", "enquiry", "about", "terms", "privacy", "plans",
                "sources", "me", "staff", "admin", "account", "ur", "prefs", "optout", "healthz", "static"}


class TaxonomyError(ValueError):
    pass


@transaction.atomic
def create_concept(*, kind, name, language="en", slug=None, parent=None, synonyms=(), **extra):
    slug = slug or slugify(name)
    if kind == Concept.Kind.LIST_TYPE:
        if slug in SYSTEM_SLUGS or ReservedSlug.objects.filter(slug=slug, kind__in=["place", "system"]).exists():
            raise TaxonomyError(f"slug {slug!r} collides with a place or system address")
    concept = Concept.objects.create(kind=kind, slug=slug, parent=parent, **extra)
    ConceptLabel.objects.create(concept=concept, language=language, kind="preferred", text=name, text_fold=fold(name))
    for syn in synonyms:
        text, lang = (syn, language) if isinstance(syn, str) else syn
        ConceptLabel.objects.create(concept=concept, language=lang, kind="synonym", text=text, text_fold=fold(text))
    if kind == Concept.Kind.LIST_TYPE:
        ReservedSlug.objects.get_or_create(slug=slug, kind="list_type")
        ListTypeSettings.objects.get_or_create(concept=concept)
    return concept


def find_concepts(query, kind=Concept.Kind.LIST_TYPE):
    """Synonym lookup: "gas station" finds the petrol-pump concept."""
    folded = fold(query)
    return Concept.objects.filter(kind=kind, labels__text_fold=folded).distinct()


@transaction.atomic
def bump_template(template, changed_by=""):
    template.version += 1
    template.save(update_fields=["version"])
    RegistryVersion.objects.create(registry_key=f"addon:{template.key}", version=template.version, changed_by=changed_by)
    return template.version


def validate_addons(template, values, *, for_publish=False):
    """Return a list of (field_key, message). Empty list means valid."""
    problems = []
    fields = {f.key: f for f in AddonField.objects.filter(template=template, deprecated_at__isnull=True)}
    for key in values:
        if key not in fields:
            problems.append((key, "unknown field"))
    for key, f in fields.items():
        val = values.get(key)
        empty = val in (None, "", [], {})
        if empty:
            if for_publish and f.required_for_publish:
                problems.append((key, "required"))
            continue
        msg = _check_value(f, val)
        if msg:
            problems.append((key, msg))
    return problems


def _check_value(field, val):
    t, rules = field.type, field.validation or {}
    if t == AddonField.Type.ENUM:
        return None if val in rules.get("choices", []) else "not an allowed choice"
    if t == AddonField.Type.BOOL:
        return None if isinstance(val, bool) else "must be true or false"
    if t == AddonField.Type.NUMBER:
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            return "must be a number"
        if "min" in rules and val < rules["min"]:
            return "below minimum"
        if "max" in rules and val > rules["max"]:
            return "above maximum"
        return None
    if t == AddonField.Type.TEXT:
        if not isinstance(val, str):
            return "must be text"
        return "too long" if len(val) > rules.get("max_length", 500) else None
    if t in (AddonField.Type.CONCEPT_LIST, AddonField.Type.IDENTIFIER_LIST, AddonField.Type.PLACE_LIST):
        return None if isinstance(val, list) else "must be a list"
    if t == AddonField.Type.MONEY:
        ok = isinstance(val, dict) and isinstance(val.get("minor"), int) and isinstance(val.get("currency"), str)
        return None if ok else "must have integer minor units and a currency"
    if t == AddonField.Type.DATE:
        return None if isinstance(val, str) and len(val) == 10 else "must be an ISO date"
    return None


def seed_manufacturer_template():
    """The pilot add-on block (plan appendix C.8). Safe to run twice."""
    tpl, _ = AddonTemplate.objects.get_or_create(key="manufacturers", defaults={"description": "Manufacturers and exporters"})
    spec = [
        ("business_type", "enum", {"choices": ["manufacturer", "trader", "wholesaler", "exporter"]}, True, "P", True, True),
        ("product_categories", "concept_list", {}, True, "P", True, False),
        ("tax_ids", "identifier_list", {}, False, "P", False, False),
        ("year_established", "number", {"min": 1800, "max": 2100}, False, "P", False, False),
        ("years_exporting", "number", {"min": 0, "max": 200}, False, "P", False, False),
        ("export_markets", "place_list", {}, False, "L", True, False),
        ("certifications", "identifier_list", {}, False, "L", True, False),
        ("verification_tier", "enum", {"choices": ["none", "documents", "on_site", "third_party"]}, False, "P", True, False),
        ("capacity_band", "enum", {"choices": ["small", "medium", "large"]}, False, "L", False, False),
        ("workforce_band", "enum", {"choices": ["1-10", "11-50", "51-200", "201-1000", "1000+"]}, False, "L", False, False),
        ("oem", "bool", {}, False, "P", True, False),
        ("moq", "text", {"max_length": 80}, False, "L", False, False),
    ]
    for key, typ, validation, req, show, filt, row in spec:
        AddonField.objects.get_or_create(template=tpl, key=key, defaults={
            "label_key": f"addon.manufacturers.{key}", "type": typ, "validation": validation,
            "required_for_publish": req, "show": show, "filterable": filt, "row_descriptor": row})
    return tpl
