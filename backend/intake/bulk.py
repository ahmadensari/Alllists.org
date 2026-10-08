"""Bulk upload pipeline (requirements BU-*): stage, score, quarantine personal rows, audit a sample, publish in
chunks, roll back.

Large lists never go straight to entries. Staging writes only ImportRow records (no entries, nothing public). A sample of
rows is checked by a person; the batch publishes as drafts only if the sample is accurate enough. Rows that look like
named individuals are held and never published by this path. Every step is resumable and recorded.
"""

import math
import random
import re

from django.db import transaction
from django.utils import timezone

from core.models import audit
from entries import services as es

from . import importer
from .gate import assert_allowed
from .models import ImportBatch, ImportRow

CHUNK = 2000
SAMPLE_CONFIDENCE_SIZE = 385  # 95% confidence, 5% margin for a large batch
ACCURACY_BAR = 0.90
MAX_ROWS_WITHOUT_COUNSEL = 1_000_000
SMALL_BATCH = 200  # at or below this every row is checked, so the sample is the whole batch

PERSONAL_DOMAINS = ("gmail.", "yahoo.", "hotmail.", "outlook.", "icloud.", "live.", "proton")
BUSINESS_WORDS = re.compile(
    r"\b(ltd|limited|pvt|private|llc|inc|co|company|corp|traders|enterprises|industries|works|centre|center|hospital|clinic|"
    r"school|hotel|store|shop|mart|services|associates|group|factory|mills|laboratory|lab|pharmacy|bakery|academy)\b",
    re.IGNORECASE,
)


class BulkError(ValueError):
    pass


def sample_size(n_rows):
    if n_rows <= SMALL_BATCH:
        return n_rows
    # finite-population correction on the 385 base
    return min(n_rows, math.ceil(SAMPLE_CONFIDENCE_SIZE / (1 + (SAMPLE_CONFIDENCE_SIZE - 1) / n_rows)))


def looks_personal(norm, concept_is_individual=False):
    """True when a row probably describes a named person rather than a business: a personal email address, or a
    two or three word name with no business word and no address or website. Held for counsel and consent,
    never published here."""
    if concept_is_individual:
        return True
    if any(e.split("@")[-1].startswith(PERSONAL_DOMAINS) for e in norm["emails"]):
        return True
    words = norm["name"].split()
    return 2 <= len(words) <= 3 and not BUSINESS_WORDS.search(norm["name"]) and not norm["address"] and not norm["website"]


def row_quality(norm):
    """Completeness from 0 to 1: a name is the minimum; phone, address, website, specialities add to it."""
    if not norm["name"]:
        return 0.0
    parts = [bool(norm["phones"]), bool(norm["address"]), bool(norm["website"]), bool(norm["specialities"])]
    return round(0.4 + 0.6 * sum(parts) / len(parts), 3)


def stage(batch, actor=None):
    """Parse and score every row without creating entries. Resumable: a stopped run continues at `staged_through`."""
    if not batch.declared_rights:
        raise BulkError("the uploader must declare the right to share this list")
    assert_allowed(batch.source, "import")
    headers, rows = importer.parse_table(batch.raw_text)
    if len(rows) > MAX_ROWS_WITHOUT_COUNSEL:
        raise BulkError("batch is larger than the limit allowed without counsel review")
    batch.mapping = batch.mapping or importer.guess_mapping(headers)
    if "name" not in batch.mapping.values():
        batch.status, batch.counts = ImportBatch.Status.FAILED, {"error": "no name column found"}
        batch.save()
        raise BulkError("could not find a name column; set the mapping")
    individual = batch.concept.settings.is_individual or batch.concept.settings.is_child_facing
    country = batch.place.country_code
    for start in range(batch.staged_through, len(rows), CHUNK):
        chunk, objs = rows[start : start + CHUNK], []
        for offset, raw in enumerate(chunk):
            norm = importer.normalise_row(raw, batch.mapping, country)
            quality = row_quality(norm)
            if not norm["name"]:
                status, msg = ImportRow.Status.ERROR, "no name"
            elif looks_personal(norm, individual):
                status, msg = ImportRow.Status.HELD, "looks like a named person; held for consent review"
            else:
                status, msg = ImportRow.Status.STAGED, ""
            objs.append(
                ImportRow(
                    batch=batch,
                    line_no=start + offset + 2,
                    raw=raw,
                    normalised=norm,
                    status=status,
                    quality=quality,
                    message=msg,
                )
            )
        with transaction.atomic():
            ImportRow.objects.bulk_create(objs)
            batch.staged_through = start + len(chunk)
            batch.save(update_fields=["staged_through"])
    return _summarise(batch, actor)


def _summarise(batch, actor):
    rows = batch.rows
    staged = rows.filter(status=ImportRow.Status.STAGED)
    counts = {
        "rows": batch.staged_through,
        "staged": staged.count(),
        "held": rows.filter(status=ImportRow.Status.HELD).count(),
        "error": rows.filter(status=ImportRow.Status.ERROR).count(),
    }
    q = [r for r in staged.values_list("quality", flat=True)]
    batch.quality = round(sum(q) / len(q), 3) if q else 0.0
    batch.counts, batch.status = counts, ImportBatch.Status.STAGED
    batch.save(update_fields=["counts", "status", "quality"])
    audit("bulk.staged", actor=actor, object_type="import_batch", object_uid=str(batch.pk), payload=counts)
    return counts


def draw_sample(batch, seed=None):
    """Pick the rows a person must check. Seeded for repeatability; stored on the batch."""
    ids = list(batch.rows.filter(status=ImportRow.Status.STAGED).values_list("line_no", flat=True))
    if not ids:
        raise BulkError("nothing staged to sample")
    rng = random.Random(seed if seed is not None else batch.pk)
    batch.audit_sample = sorted(rng.sample(ids, sample_size(len(ids))))
    batch.save(update_fields=["audit_sample"])
    return batch.audit_sample


def record_audit(batch, results, actor=None):
    """`results` maps line number to True (row is correct) or False. Every sampled row must be judged.
    The batch passes when accuracy reaches the bar; otherwise it is rejected and cannot be published."""
    missing = [n for n in batch.audit_sample if n not in results]
    if not batch.audit_sample or missing:
        raise BulkError(f"{len(missing)} sampled rows have no result" if batch.audit_sample else "draw a sample first")
    ok = sum(1 for n in batch.audit_sample if results[n])
    batch.accuracy = round(ok / len(batch.audit_sample), 4)
    batch.status = ImportBatch.Status.AUDITED if batch.accuracy >= ACCURACY_BAR else ImportBatch.Status.REJECTED
    batch.save(update_fields=["accuracy", "status"])
    audit(
        "bulk.audited",
        actor=actor,
        object_type="import_batch",
        object_uid=str(batch.pk),
        payload={"accuracy": batch.accuracy, "sample": len(batch.audit_sample), "status": batch.status},
    )
    return batch.accuracy


def publish(batch, actor=None, addons=None):
    """Create draft entries for staged rows in chunks. Needs a passed audit. Held and error rows are never published.
    Resumable at `published_through`. Entries stay drafts and earn nothing until verified (R08, R09)."""
    if batch.status not in (ImportBatch.Status.AUDITED, ImportBatch.Status.DONE):
        raise BulkError("the sample audit has not passed")
    todo = batch.rows.filter(status=ImportRow.Status.STAGED, line_no__gt=batch.published_through).order_by("line_no")
    made = dup = err = 0
    for row in todo.iterator(chunk_size=CHUNK):
        norm = row.normalised
        contacts = [("phone", p) for p in dict.fromkeys(norm["phones"])] + [("email", e) for e in norm["emails"]]
        extra = {"addons": addons} if addons else {}
        try:
            with transaction.atomic():
                entry = es.create_entry(
                    name=norm["name"],
                    place=batch.place,
                    primary_concept=batch.concept,
                    created_by=batch.uploader,
                    created_via="import",
                    source=batch.source,
                    address_text=norm["address"],
                    website=norm["website"],
                    contacts=contacts,
                    **extra,
                )
                entry, outcome = importer.settle_duplicate(entry, actor)
        except es.EntryError as exc:
            row.status, row.message = ImportRow.Status.ERROR, str(exc)[:200]
            err += 1
        else:
            row.entry = entry
            row.status = ImportRow.Status.DUPLICATE if outcome == "merged" else ImportRow.Status.DRAFTED
            row.message = f"merged into {entry.uid}" if outcome == "merged" else ""
            dup += outcome == "merged"
            made += outcome != "merged"
        row.save(update_fields=["status", "message", "entry"])
        batch.published_through = row.line_no
        batch.save(update_fields=["published_through"])
    batch.status, batch.finished_at = ImportBatch.Status.DONE, timezone.now()
    drafted = batch.rows.filter(status=ImportRow.Status.DRAFTED).count()
    counts = dict(batch.counts, drafted=drafted, duplicates=dup, errors_on_publish=err)
    batch.counts = counts
    batch.save(update_fields=["status", "finished_at", "counts"])
    audit("bulk.published", actor=actor, object_type="import_batch", object_uid=str(batch.pk), payload=counts)
    return counts


def rollback(batch, actor=None, reason=""):
    """Withdraw what this batch created: drafts that nobody has verified are soft-deleted. Verified or published
    entries are left alone and counted so a person can handle them."""
    from entries.models import Entry

    withdrawn = kept = 0
    now = timezone.now()
    for row in batch.rows.filter(status=ImportRow.Status.DRAFTED).select_related("entry"):
        e = row.entry
        if e and e.deleted_at is None and e.publish_state == Entry.PublishState.DRAFT and not e.verification_events.exists():
            e.deleted_at, e.tombstone_reason = now, f"bulk rollback {batch.pk}: {reason}"[:80]
            e.save(update_fields=["deleted_at", "tombstone_reason"])
            row.status, row.message = ImportRow.Status.ERROR, "rolled back"
            row.save(update_fields=["status", "message"])
            withdrawn += 1
        else:
            kept += 1
    batch.status = ImportBatch.Status.ROLLED_BACK
    batch.save(update_fields=["status"])
    audit(
        "bulk.rolled_back",
        actor=actor,
        object_type="import_batch",
        object_uid=str(batch.pk),
        payload={"withdrawn": withdrawn, "kept": kept, "reason": reason},
    )
    return {"withdrawn": withdrawn, "kept": kept}
