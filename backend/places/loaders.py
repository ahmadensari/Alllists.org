"""Place-tree loaders from open data held in local files (plan P1.06). Nothing here uses the network: download the files
first (GeoNames dumps, or Overture divisions converted to JSON lines) and point the loader at them.

Both loaders are repeatable: a place that already carries the external id is updated, never duplicated."""

import csv
import io
import json

from django.db import transaction

from core.models import audit
from places.services import PlaceError, create_place, make_slug
from taxonomy.services import SYSTEM_SLUGS
from taxonomy.models import ReservedSlug

from .models import Place, PlaceExternalId, PlaceName

GEONAMES_CITY_CLASSES = {"P"}
OVERTURE_LEVELS = {
    "country": Place.Level.COUNTRY,
    "region": Place.Level.ADMIN1,
    "county": Place.Level.ADMIN2,
    "localadmin": Place.Level.ADMIN3,
    "locality": Place.Level.CITY,
    "borough": Place.Level.AREA,
    "neighborhood": Place.Level.AREA,
    "macrohood": Place.Level.AREA,
}


class LoaderError(ValueError):
    pass


def _rows(text, min_cols=1):
    for line in io.StringIO(text):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= min_cols:
            yield parts


def _unique_slug(parent, name, suffix):
    base = make_slug(name)
    taken = set(Place.objects.filter(parent=parent).values_list("slug", flat=True))
    if base in taken or ReservedSlug.objects.filter(slug=base, kind="list_type").exists() or base in SYSTEM_SLUGS:
        return f"{base}-{suffix}"
    return base


def _world():
    return Place.objects.filter(level="world").first() or create_place(
        parent=None, level=Place.Level.WORLD, name="World", slug="world"
    )


def _set_names(place, names):
    """names: [(language, text)]. Adds missing names, never removes."""
    from core.textfold import fold

    have = {(n.language, n.name) for n in place.names.all()}
    for lang, text in names:
        text = (text or "").strip()
        if text and (lang, text) not in have:
            PlaceName.objects.create(place=place, language=lang, name=text, name_fold=fold(text))
            have.add((lang, text))


def _find_ext(scheme, value):
    row = PlaceExternalId.objects.filter(scheme=scheme, value=str(value)).select_related("place").first()
    return row.place if row else None


def _link(place, scheme, value):
    PlaceExternalId.objects.get_or_create(place=place, scheme=scheme, value=str(value))


@transaction.atomic
def load_geonames(
    *, country_info, admin1, places, alternate_names="", country=None, min_population=15000, languages=("ur",)
):
    """Load countries, first-level divisions and cities from GeoNames text. `country` limits to one ISO code.

    country_info: contents of countryInfo.txt. admin1: admin1CodesASCII.txt. places: a GeoNames place dump
    (cities15000.txt or one country file). alternate_names: alternateNamesV2 rows for translated names, optional.
    Returns counts."""
    country = country.upper() if country else None
    counts = {"countries": 0, "regions": 0, "cities": 0, "updated": 0, "skipped": 0}
    world = _world()
    alt = {}
    for parts in _rows(alternate_names, 4):
        if parts[2] in languages:
            alt.setdefault(parts[1], []).append((parts[2], parts[3]))
    countries = {}
    for p in _rows(country_info, 5):
        iso, name, gid = p[0], p[4], p[16] if len(p) > 16 else ""
        if country and iso != country:
            continue
        place = Place.objects.filter(level="country", country_code=iso).first()
        if place is None:
            place = create_place(parent=world, level=Place.Level.COUNTRY, name=name, country_code=iso, iso_code=iso)
            counts["countries"] += 1
        else:
            counts["updated"] += 1
        if gid.isdigit():
            Place.objects.filter(pk=place.pk).update(geonames_id=int(gid))
            _set_names(place, alt.get(gid, []))
        countries[iso] = place
    regions = {}
    for p in _rows(admin1, 4):
        code, name, gid = p[0], p[1], p[3]
        iso = code.split(".")[0]
        if iso not in countries:
            continue
        place = _find_ext("geonames", gid)
        if place is None:
            place = create_place(
                parent=countries[iso],
                level=Place.Level.ADMIN1,
                name=name,
                slug=_unique_slug(countries[iso], name, code.split(".")[-1].lower()),
                iso_code=code,
                geonames_id=int(gid),
            )
            _link(place, "geonames", gid)
            counts["regions"] += 1
        else:
            counts["updated"] += 1
        _set_names(place, alt.get(gid, []))
        regions[code] = place
    for p in _rows(places, 15):
        gid, name, lat, lon, fclass, iso, adm1, pop = p[0], p[1], p[4], p[5], p[6], p[8], p[10], p[14]
        if iso not in countries or fclass not in GEONAMES_CITY_CLASSES or int(pop or 0) < min_population:
            counts["skipped"] += 1
            continue
        parent = regions.get(f"{iso}.{adm1}") or countries[iso]
        place = _find_ext("geonames", gid)
        if place is None:
            place = create_place(
                parent=parent,
                level=Place.Level.CITY,
                name=name,
                slug=_unique_slug(parent, name, gid),
                geonames_id=int(gid),
                centre_lat=lat,
                centre_lon=lon,
                population_band=_band(int(pop or 0)),
            )
            _link(place, "geonames", gid)
            counts["cities"] += 1
        else:
            counts["updated"] += 1
        _set_names(place, alt.get(gid, []))
    audit("places.load", object_type="geonames", object_uid=country or "all", payload=counts)
    return counts


def _band(pop):
    return "1m+" if pop >= 1_000_000 else "100k+" if pop >= 100_000 else "15k+" if pop >= 15_000 else "small"


@transaction.atomic
def load_overture_divisions(lines, *, country=None):
    """Load Overture `division` records given as JSON lines (convert the Parquet release first).

    Needs, per record: id, subtype, names.primary, optional names.common.{lang}, country, and parent_division_id.
    Records are applied parents first; a record whose parent is unknown is skipped and counted."""
    country = country.upper() if country else None
    recs = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        props = r.get("properties", r)  # accept GeoJSON features and flat records
        if props.get("subtype") not in OVERTURE_LEVELS:
            continue
        if country and (props.get("country") or "").upper() != country:
            continue
        recs.append(props)
    counts = {"created": 0, "updated": 0, "skipped_no_parent": 0}
    world = _world()
    pending = sorted(recs, key=lambda p: list(OVERTURE_LEVELS).index(p["subtype"]))
    for _ in range(6):  # a few passes so children can follow parents regardless of file order
        left = []
        for p in pending:
            names = p.get("names", {}) or {}
            primary = names.get("primary") or ""
            if not primary:
                continue
            level = OVERTURE_LEVELS[p["subtype"]]
            existing = _find_ext("overture", p["id"])
            if existing is not None:
                _set_names(existing, [(lg, t) for lg, t in (names.get("common") or {}).items() if lg in ("ur", "en")])
                counts["updated"] += 1
                continue
            if level == Place.Level.COUNTRY:
                parent = world
            else:
                parent = _find_ext("overture", p.get("parent_division_id") or "")
                if parent is None:
                    left.append(p)
                    continue
            try:
                place = create_place(
                    parent=parent,
                    level=level,
                    name=primary,
                    slug=_unique_slug(parent, primary, p["id"][-6:]),
                    country_code=(p.get("country") or "").upper(),
                    names=[(lg, t) for lg, t in (names.get("common") or {}).items() if lg == "ur"],
                )
            except PlaceError:
                continue
            _link(place, "overture", p["id"])
            counts["created"] += 1
        if not left or len(left) == len(pending):
            counts["skipped_no_parent"] = len(left)
            break
        pending = left
    audit("places.load", object_type="overture", object_uid=country or "all", payload=counts)
    return counts


def parse_tsv(text):
    return list(csv.reader(io.StringIO(text), delimiter="\t"))
