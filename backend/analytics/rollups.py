"""Roll-up cells (plan 4.4). Each changed entry touches its place ancestors times its concept ancestors."""
from datetime import timedelta

from django.db import transaction

from core import clock
from entries.models import Entry
from entries.services import current_level
from taxonomy.models import Concept

from .models import RollupCell


def place_paths(path):
    """'pk.punjab.sialkot' -> ['', 'pk', 'pk.punjab', 'pk.punjab.sialkot'] (world is the empty path)."""
    parts = path.split(".") if path else []
    return [""] + [".".join(parts[:i]) for i in range(1, len(parts) + 1)]


def concept_chain(concept):
    chain = []
    while concept is not None:
        chain.append(concept.pk)
        concept = concept.parent
    return chain


def _entries_in(path, concept_ids, country):
    qs = Entry.objects.filter(primary_concept_id__in=concept_ids, deleted_at__isnull=True, merged_into__isnull=True)
    if country:
        qs = qs.filter(country_code=country)
    if path:
        qs = [e for e in qs.filter(place_path__startswith=path)
              if e.place_path == path or e.place_path.startswith(path + ".")]
    return list(qs)


def descendant_concept_ids(concept_id):
    ids, frontier = [concept_id], [concept_id]
    while frontier:
        frontier = list(Concept.objects.filter(parent_id__in=frontier).values_list("pk", flat=True))
        ids += frontier
    return ids


@transaction.atomic
def recount_cell(country, path, concept_id, now=None):
    now = now or clock.now()
    entries = _entries_in(path, descendant_concept_ids(concept_id), country)
    if not entries:
        RollupCell.objects.filter(country_code=country, place_path=path, concept_id=concept_id).delete()
        return None
    published = [e for e in entries if e.publish_state == Entry.PublishState.PUBLISHED]
    by_level = {"surveyor": 0, "owner": 0, "ai": 0, "none": 0}
    verified_12m = 0
    for e in published:
        by_level[current_level(e, now)] += 1
        if e.last_verified_at and e.last_verified_at > now - timedelta(days=365):
            verified_12m += 1
    with_contact = sum(1 for e in published if e.contact_set.exists())
    cell, _ = RollupCell.objects.update_or_create(
        country_code=country, place_path=path, concept_id=concept_id,
        defaults=dict(total=len(entries), published=len(published), by_level=by_level, verified_12m=verified_12m,
                      with_contact_pct=round(100 * with_contact / len(published)) if published else 0,
                      updated_at=now))
    return cell


def refresh_for_entry(entry, now=None):
    """Incremental update after an entry changed."""
    for path in place_paths(entry.place_path):
        for cid in concept_chain(entry.primary_concept):
            recount_cell(entry.country_code, path, cid, now)


def recount_all(now=None):
    """Exact nightly recount. Returns the number of cells now present."""
    seen = set()
    for e in Entry.objects.filter(deleted_at__isnull=True, merged_into__isnull=True).select_related("primary_concept"):
        for path in place_paths(e.place_path):
            for cid in concept_chain(e.primary_concept):
                if (e.country_code, path, cid) not in seen:
                    seen.add((e.country_code, path, cid))
                    recount_cell(e.country_code, path, cid, now)
    stale = RollupCell.objects.all()
    for cell in stale:
        if (cell.country_code, cell.place_path, cell.concept_id) not in seen:
            cell.delete()
    return len(seen)
