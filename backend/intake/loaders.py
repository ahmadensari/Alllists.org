"""Bulk loaders for open place datasets (plan P1.19): Overture places (JSON lines), Foursquare Open Source Places
(TSV or CSV) and a generic CSV. Files are local; nothing is fetched.

Rules, all enforced here and not left to the caller:
- the source must allow `import` (the gate), and every record becomes a DRAFT with no credit (rules R08, R09);
- a record whose category does not map to one of our list types is counted and skipped, never guessed;
- a record needs a name and a place we already have; the nearest known city or area within MAX_KM is used;
- the loader is resumable: each record id is written to `ExternalRecord`, and a rerun skips what is already there;
- duplicates go through the same pipeline as a paste import."""

import csv
import io
import json
import math

from core.models import audit
from entries import services as es
from entries.models import Entry
from places.models import Place
from taxonomy.loaders import concept_for_code

from .gate import SourceBlocked, assert_allowed
from .importer import settle_duplicate
from .models import ExternalRecord

MAX_KM = 25.0


def _km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


class PlaceIndex:
    """Cities and areas of one country with a centre point, for nearest-place lookup. Built once per load."""

    def __init__(self, country):
        qs = Place.objects.filter(country_code=country, status="active", centre_lat__isnull=False)
        self.items = [(float(p.centre_lat), float(p.centre_lon), p) for p in qs]

    def nearest(self, lat, lon):
        """The closest centre within MAX_KM; among centres within 3 km of the closest, the deepest (an area over its city)."""
        near = sorted(((_km(lat, lon, a, b), place) for a, b, place in self.items), key=lambda t: t[0])
        near = [t for t in near if t[0] <= MAX_KM]
        if not near:
            return None
        closest = near[0][0]
        return max((t for t in near if t[0] <= closest + 3), key=lambda t: (t[1].depth, -t[0]))[1]


# ---- readers: each yields dicts with id, name, lat, lon, address, phone, website, category, local_names -------------------


def read_overture_places(lines):
    for line in lines:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        props = r.get("properties", r)
        geom = r.get("geometry") or props.get("geometry") or {}
        coords = geom.get("coordinates") or [None, None]
        names = props.get("names") or {}
        addr = (props.get("addresses") or [{}])[0] or {}
        yield {
            "id": r.get("id") or props.get("id"),
            "name": names.get("primary") or "",
            "lat": coords[1],
            "lon": coords[0],
            "address": ", ".join(x for x in (addr.get("freeform"), addr.get("locality")) if x),
            "phone": (props.get("phones") or [""])[0],
            "website": (props.get("websites") or [""])[0],
            "category": ((props.get("categories") or {}) or {}).get("primary") or "",
            "system": "overture",
            "local_names": [(lg, t) for lg, t in (names.get("common") or {}).items() if lg == "ur"],
        }


def read_foursquare_places(text):
    first = text.splitlines()[0] if text else ""
    dialect = csv.excel_tab if "\t" in first else csv.excel
    for row in csv.DictReader(io.StringIO(text), dialect=dialect):
        ids = (row.get("fsq_category_ids") or row.get("fsq_category_id") or "").strip("[] ").replace("'", "")
        cat = next((c.strip() for c in ids.split(",") if c.strip()), "")
        try:
            lat, lon = float(row.get("latitude")), float(row.get("longitude"))
        except (TypeError, ValueError):
            lat = lon = None
        yield {
            "id": row.get("fsq_place_id") or row.get("fsq_id") or "",
            "name": (row.get("name") or "").strip(),
            "lat": lat,
            "lon": lon,
            "address": ", ".join(x for x in (row.get("address"), row.get("locality")) if x),
            "phone": row.get("tel") or "",
            "website": row.get("website") or "",
            "category": cat,
            "system": "foursquare",
            "local_names": [],
        }


def read_generic_csv(text, system="own"):
    for i, row in enumerate(csv.DictReader(io.StringIO(text))):
        try:
            lat, lon = float(row.get("lat")), float(row.get("lon"))
        except (TypeError, ValueError):
            lat = lon = None
        yield {
            "id": row.get("id") or f"row-{i}",
            "name": (row.get("name") or "").strip(),
            "lat": lat,
            "lon": lon,
            "address": row.get("address") or "",
            "phone": row.get("phone") or "",
            "website": row.get("website") or "",
            "category": row.get("category") or "",
            "system": system,
            "local_names": [],
        }


def load_places(source, records, *, country, actor=None, limit=None):
    """Create draft entries from normalised records. Returns outcome counts."""
    assert_allowed(source, "import")  # raises SourceBlocked before anything is written
    index = PlaceIndex(country.upper())
    counts = {"seen": 0, "drafted": 0, "merged": 0, "possible_duplicate": 0}
    done = 0
    for rec in records:
        if limit is not None and done >= limit:
            break
        counts["seen"] += 1
        ext = str(rec["id"] or "")
        if not ext or ExternalRecord.objects.filter(source=source, external_id=ext).exists():
            continue
        outcome, entry = _one(source, rec, index, actor)
        ExternalRecord.objects.create(source=source, external_id=ext, entry=entry, outcome=outcome)
        counts[outcome] = counts.get(outcome, 0) + 1
        done += 1
    audit("places.bulk_load", actor=actor, object_type="source", object_uid=str(source.pk), payload=counts)
    return counts


def _one(source, rec, index, actor):
    if not rec["name"]:
        return "no_name", None
    concept = concept_for_code(rec["system"], rec["category"])
    if concept is None or concept.kind != "list_type":
        return "no_category", None
    if rec["lat"] is None or rec["lon"] is None:
        return "no_place", None
    place = index.nearest(rec["lat"], rec["lon"])
    if place is None:
        return "no_place", None
    contacts = [("phone", rec["phone"])] if rec["phone"] else []
    try:
        entry = es.create_entry(
            name=rec["name"],
            place=place,
            primary_concept=concept,
            created_via=Entry.CreatedVia.IMPORT,
            source=source,
            address_text=rec["address"][:400],
            website=rec["website"] if str(rec["website"]).startswith("http") else "",
            contacts=contacts,
            lat=round(rec["lat"], 6),
            lon=round(rec["lon"], 6),
            name_variants=[(t, lg, "transliteration") for lg, t in rec["local_names"]],
        )
    except SourceBlocked:
        raise
    except es.EntryError:
        return "blocked", None
    entry, state = settle_duplicate(entry, actor)
    return ("merged" if state == "merged" else "possible_duplicate" if state == "possible" else "drafted"), entry
