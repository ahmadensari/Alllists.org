"""Search (plan 10.1): fold the query, find list types by synonym, places by name, and entries by name inside a scope.
Unscoped search never scans entry names (150 to 520 ms at a million entries); it looks up list types and places only."""

from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import Q

from core.textfold import fold
from entries.models import NameVariant
from places.models import Place, PlaceName
from taxonomy.models import Concept, ConceptLabel

from . import queries

MIN_QUERY = 2
LABEL_SIM = 0.35
ENTRY_SIM = 0.25


def _pg():
    return connection.vendor == "postgresql"


def concepts(qf):
    qs = ConceptLabel.objects.filter(concept__kind="list_type", concept__status="active")
    if _pg():
        qs = (
            qs.annotate(sim=TrigramSimilarity("text_fold", qf))
            .filter(Q(sim__gte=LABEL_SIM) | Q(text_fold=qf))
            .order_by("-sim")
        )
    else:
        qs = qs.filter(text_fold__icontains=qf)
    seen, out = set(), []
    for lb in qs.select_related("concept")[:30]:
        if lb.concept_id not in seen:
            seen.add(lb.concept_id)
            out.append(lb.concept)
    return out[:10]


def places(qf):
    qs = PlaceName.objects.filter(place__status="active").exclude(place__level="world")
    if _pg():
        qs = (
            qs.annotate(sim=TrigramSimilarity("name_fold", qf))
            .filter(Q(sim__gte=LABEL_SIM) | Q(name_fold=qf))
            .order_by("-sim")
        )
    else:
        qs = qs.filter(name_fold__icontains=qf)
    seen, out = set(), []
    for pn in qs.select_related("place")[:30]:
        if pn.place_id not in seen:
            seen.add(pn.place_id)
            out.append(pn.place)
    return out[:10]


def entries(qf, scope_place, limit=25):
    """Entry names inside a scope only."""
    qs = (
        queries.published_entries(scope_place)
        .select_related("place", "primary_concept")
        .prefetch_related("verification_current", "place__names")
    )
    if _pg():
        variant_ids = (
            NameVariant.objects.annotate(sim=TrigramSimilarity("text_fold", qf))
            .filter(sim__gte=ENTRY_SIM)
            .values("entry_id")
        )
        qs = (
            qs.annotate(sim=TrigramSimilarity("name_fold", qf))
            .filter(Q(sim__gte=ENTRY_SIM) | Q(id__in=variant_ids) | Q(name_fold__contains=qf))
            .order_by("-sim", "name_fold")
        )
    else:
        qs = (
            qs.filter(Q(name_fold__contains=qf) | Q(namevariant_set__text_fold__contains=qf))
            .distinct()
            .order_by("name_fold")
        )
    return list(qs[:limit])


def run(query, scope_place=None):
    """Return a dict of result groups. Short queries return nothing."""
    q = (query or "").strip()
    qf = fold(q)
    out = {"query": q, "concepts": [], "places": [], "entries": [], "scope": scope_place}
    if len(qf) < MIN_QUERY:
        return out
    out["concepts"] = concepts(qf)
    out["places"] = places(qf)
    if scope_place is not None:
        out["entries"] = entries(qf, scope_place)
    return out


def total(results):
    return len(results["concepts"]) + len(results["places"]) + len(results["entries"])


def scope_from_path(path):
    if not path:
        return None
    return Place.objects.filter(path=path, status="active").first()


__all__ = ["run", "total", "scope_from_path", "Concept"]
