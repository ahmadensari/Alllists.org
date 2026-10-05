"""Search backends behind one interface (plan 10.1, P6.01).

A backend answers three questions with already folded text: which list types match a query, which places match, and
which entries inside one scope match. `ModelBackend` uses PostgreSQL trigram search on the tables (the default).
`MemoryBackend` is a second, independent implementation used to prove the contract; a dedicated search engine adapter
(Meilisearch, Typesense, OpenSearch) is a third class with the same three methods, chosen with `SEARCH_BACKEND`.
The same contract tests must pass on every backend (catalog/tests/test_search_backends.py)."""

from importlib import import_module

from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.db import connection
from django.db.models import Q

from entries.models import NameVariant
from places.models import Place, PlaceName
from taxonomy.models import ConceptLabel

from . import queries

MIN_QUERY = 2
LABEL_SIM = 0.35
ENTRY_SIM = 0.25


def get_backend():
    path = getattr(settings, "SEARCH_BACKEND", "catalog.search_backend.ModelBackend")
    module, _, name = path.rpartition(".")
    return getattr(import_module(module), name)()


class ModelBackend:
    """Trigram search in PostgreSQL (substring match on other databases, used only in quick local runs)."""

    @staticmethod
    def _pg():
        return connection.vendor == "postgresql"

    def concepts(self, qf):
        qs = ConceptLabel.objects.filter(concept__kind="list_type", concept__status="active")
        if self._pg():
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

    def places(self, qf):
        qs = PlaceName.objects.filter(place__status="active").exclude(place__level="world")
        if self._pg():
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

    def entries(self, qf, scope_place, limit=25):
        """Entry names inside a scope only."""
        qs = (
            queries.published_entries(scope_place)
            .select_related("place", "primary_concept")
            .prefetch_related("verification_current", "place__names")
        )
        if self._pg():
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


def trigrams(text):
    """pg_trgm's definition: each word padded with two spaces before and one after, all 3-letter windows."""
    out = set()
    for word in text.split():
        padded = f"  {word} "
        out.update(padded[i : i + 3] for i in range(len(padded) - 2))
    return out


def similarity(a, b):
    ta, tb = trigrams(a), trigrams(b)
    return (len(ta & tb) / len(ta | tb)) if ta and tb else 0.0


class MemoryBackend:
    """The same behaviour computed in Python over rows read from the tables. Slow on big data; it exists to prove that the
    interface is enough for another engine and to give tests an independent reference."""

    def concepts(self, qf):
        scored = {}
        for lb in ConceptLabel.objects.filter(concept__kind="list_type", concept__status="active").select_related(
            "concept"
        ):
            s = 1.0 if lb.text_fold == qf else similarity(lb.text_fold, qf)
            if s >= LABEL_SIM and s > scored.get(lb.concept_id, (0, None))[0]:
                scored[lb.concept_id] = (s, lb.concept)
        return [c for _, c in sorted(scored.values(), key=lambda t: -t[0])][:10]

    def places(self, qf):
        scored = {}
        for pn in (
            PlaceName.objects.filter(place__status="active").exclude(place__level="world").select_related("place")
        ):
            s = 1.0 if pn.name_fold == qf else similarity(pn.name_fold, qf)
            if s >= LABEL_SIM and s > scored.get(pn.place_id, (0, None))[0]:
                scored[pn.place_id] = (s, pn.place)
        return [p for _, p in sorted(scored.values(), key=lambda t: -t[0])][:10]

    def entries(self, qf, scope_place, limit=25):
        variants = {}
        for v in NameVariant.objects.values("entry_id", "text_fold"):
            variants.setdefault(v["entry_id"], []).append(v["text_fold"])
        out = []
        qs = (
            queries.published_entries(scope_place)
            .select_related("place", "primary_concept")
            .prefetch_related("verification_current", "place__names")
        )
        for e in qs:
            names = [e.name_fold] + variants.get(e.pk, [])
            s = max(similarity(n, qf) for n in names)
            if qf in e.name_fold or s >= ENTRY_SIM:
                out.append((s, e))
        out.sort(key=lambda t: (-t[0], t[1].name_fold))
        return [e for _, e in out[:limit]]


__all__ = ["get_backend", "ModelBackend", "MemoryBackend", "Place", "Q", "connection", "TrigramSimilarity"]
