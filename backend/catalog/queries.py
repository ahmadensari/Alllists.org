"""Read side for pages: everything is scoped by place path and concept and uses the indexes (plan 4.4, 10.3)."""

from datetime import timedelta

from django.db.models import Max, Q, Sum

from analytics.models import RollupCell
from analytics.rollups import descendant_concept_ids
from core import clock
from entries.models import Entry
from places.models import Place
from taxonomy.models import Concept

LEVEL_ORDER = ["surveyor", "owner", "ai"]


def published_entries(place, concept=None):
    qs = Entry.objects.filter(
        publish_state=Entry.PublishState.PUBLISHED, deleted_at__isnull=True, merged_into__isnull=True
    )
    if place.path:
        qs = qs.filter(Q(place_path=place.path) | Q(place_path__startswith=place.path + "."))
    if concept is not None:
        qs = qs.filter(primary_concept_id__in=descendant_concept_ids(concept.pk))
    return qs


def best_level(entry, now=None):
    """Best unexpired level from prefetched `verification_current` rows (no extra queries)."""
    now = now or clock.now()
    levels = {
        v.level
        for v in entry.verification_current.all()
        if v.state == "verified" and v.expires_at and v.expires_at > now
    }
    for lv in LEVEL_ORDER:
        if lv in levels:
            return lv
    return "none"


def rollup(place, concept):
    """Sum the cell across countries (the world path spans countries). Returns a dict, zero if no cell."""
    cells = list(RollupCell.objects.filter(place_path=place.path, concept=concept))
    out = {"total": 0, "published": 0, "by_level": {"surveyor": 0, "owner": 0, "ai": 0, "none": 0}, "updated_at": None}
    for c in cells:
        out["total"] += c.total
        out["published"] += c.published
        for k, v in c.by_level.items():
            out["by_level"][k] = out["by_level"].get(k, 0) + v
        if out["updated_at"] is None or c.updated_at > out["updated_at"]:
            out["updated_at"] = c.updated_at
    return out


def trust_split(cell):
    pub = cell["published"] or 0
    if not pub:
        return {"s": 0, "o": 0, "a": 0, "pct": 0}
    s = round(100 * cell["by_level"].get("surveyor", 0) / pub)
    o = round(100 * cell["by_level"].get("owner", 0) / pub)
    a = round(100 * cell["by_level"].get("ai", 0) / pub)
    return {"s": s, "o": o, "a": a, "pct": s + o}


def lists_here(place):
    """List-type cells at a place, biggest first."""
    return (
        RollupCell.objects.filter(place_path=place.path, concept__kind=Concept.Kind.LIST_TYPE, published__gt=0)
        .values("concept_id")
        .annotate(n=Sum("published"))
        .order_by("-n")
    )


def child_counts(place):
    """{child place id: published entries under it} from list-type cells (nested list types would double count)."""
    children = list(Place.objects.filter(parent=place, status="active").order_by("slug"))
    out = []
    for c in children:
        n = (
            RollupCell.objects.filter(place_path=c.path, concept__kind=Concept.Kind.LIST_TYPE).aggregate(
                n=Sum("published")
            )["n"]
            or 0
        )
        out.append((c, n))
    return out


def place_total(place):
    return (
        RollupCell.objects.filter(place_path=place.path, concept__kind=Concept.Kind.LIST_TYPE).aggregate(
            n=Sum("published")
        )["n"]
        or 0
    )


def area_chips(place, concept):
    """Child places of `place` that have published entries of this list type, with counts."""
    cells = RollupCell.objects.filter(
        concept=concept,
        published__gt=0,
        place_path__in=list(Place.objects.filter(parent=place, status="active").values_list("path", flat=True)),
    )
    counts = {}
    for c in cells:
        counts[c.place_path] = counts.get(c.place_path, 0) + c.published
    out = []
    for child in Place.objects.filter(parent=place, status="active", path__in=list(counts)).prefetch_related("names"):
        out.append((child, counts[child.path]))
    return sorted(out, key=lambda t: t[0].slug)


def last_checked(place, concept):
    return published_entries(place, concept).aggregate(m=Max("last_verified_at"))["m"]


def alt_name(entry, lang):
    """The entry name in the other script or language, if one is stored."""
    for v in entry.namevariant_set.all():
        if (
            v.text != entry.name
            and v.kind in ("legal", "trade", "transliteration")
            and (v.language or "") != entry.name_lang
        ):
            return v.text
    return ""


def list_rows_queryset(place, concept, area_place=None, sort="name"):
    scope_place = area_place or place
    qs = (
        published_entries(scope_place, concept)
        .select_related("place", "primary_concept")
        .prefetch_related("verification_current", "namevariant_set", "place__names")
    )
    if sort == "checked":
        return qs.order_by("-last_verified_at", "name_fold")
    return qs.order_by("name_fold", "id")


def stamp(*parts):
    """A cheap data stamp used in ETags: the newest of the given datetimes."""
    ds = [p for p in parts if p is not None]
    return max(ds).isoformat() if ds else "0"


def freshness_window():
    return clock.now() - timedelta(days=365)


def ancestors_of(place):
    """World down to `place` in one query (by path prefixes), with names prefetched."""
    from analytics.rollups import place_paths

    return list(
        Place.objects.filter(path__in=place_paths(place.path), status="active")
        .prefetch_related("names")
        .order_by("depth")
    )
