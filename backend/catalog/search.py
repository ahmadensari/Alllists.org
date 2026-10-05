"""Search (plan 10.1): fold the query, find list types by synonym, places by name, and entries by name inside a scope.
Unscoped search never scans entry names (150 to 520 ms at a million entries); it looks up list types and places only."""

from core.textfold import fold
from places.models import Place
from taxonomy.models import Concept

from .search_backend import MIN_QUERY, get_backend


def concepts(qf):
    return get_backend().concepts(qf)


def places(qf):
    return get_backend().places(qf)


def entries(qf, scope_place, limit=25):
    return get_backend().entries(qf, scope_place, limit)


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
