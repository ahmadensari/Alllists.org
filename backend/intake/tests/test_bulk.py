import pytest

from entries.models import Entry
from intake import bulk
from intake.models import ImportBatch, ImportRow
from intake.tests.test_import_dedupe import batch

pytestmark = pytest.mark.django_db

BIG = "Business Name,Mobile,Address,Website\n" + "\n".join(
    f"Unit {i} Surgical Works,03{i % 90 + 10:02d}{i:07d},Road {i},unit{i}.example.com" for i in range(1, 251)
)
PEOPLE = "Name,Mobile,Email\nAli Raza,0300 111 2222,ali@gmail.com\nCrescent Traders,0300 333 4444,sales@crescent.example\n,0300 000 0000,\n"


def test_staging_creates_no_entries_and_scores_rows(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text=BIG)
    counts = bulk.stage(b)
    assert counts["staged"] == 250 and Entry.objects.count() == 0
    b.refresh_from_db()
    assert b.status == ImportBatch.Status.STAGED and b.staged_through == 250 and 0.8 < b.quality <= 1


def test_personal_and_blank_rows_are_held_or_errored_never_published(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text=PEOPLE)
    c = bulk.stage(b)
    assert c == {"rows": 3, "staged": 1, "held": 1, "error": 1}
    bulk.draw_sample(b)
    bulk.record_audit(b, {n: True for n in b.audit_sample})
    bulk.publish(b)
    assert Entry.objects.count() == 1 and Entry.objects.get().name == "Crescent Traders"


def test_publish_needs_a_passed_audit_and_low_accuracy_rejects(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text=BIG)
    bulk.stage(b)
    with pytest.raises(bulk.BulkError):
        bulk.publish(b)
    sample = bulk.draw_sample(b)
    assert len(sample) == bulk.sample_size(250) < 250
    acc = bulk.record_audit(b, {n: i % 2 == 0 for i, n in enumerate(sample)})
    assert acc < bulk.ACCURACY_BAR
    b.refresh_from_db()
    assert b.status == ImportBatch.Status.REJECTED
    with pytest.raises(bulk.BulkError):
        bulk.publish(b)


def test_audit_requires_every_sampled_row_judged(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text=BIG)
    bulk.stage(b)
    sample = bulk.draw_sample(b)
    with pytest.raises(bulk.BulkError):
        bulk.record_audit(b, {sample[0]: True})


def test_publish_resumes_and_rollback_withdraws_unverified_drafts(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text=BIG)
    bulk.stage(b)
    sample = bulk.draw_sample(b)
    bulk.record_audit(b, {n: True for n in sample})
    bulk.publish(b)
    n = Entry.objects.filter(deleted_at__isnull=True).count()
    assert n == 250
    again = bulk.publish(b)  # nothing left to do, no duplicates created
    assert Entry.objects.filter(deleted_at__isnull=True).count() == n and again["errors_on_publish"] == 0
    res = bulk.rollback(b, reason="test")
    assert res == {"withdrawn": 250, "kept": 0}
    assert Entry.objects.filter(deleted_at__isnull=True).count() == 0
    b.refresh_from_db()
    assert b.status == ImportBatch.Status.ROLLED_BACK


def test_staging_is_resumable_from_checkpoint(tree, surgical, users, green, monkeypatch):
    monkeypatch.setattr(bulk, "CHUNK", 100)
    b = batch(tree, surgical, users, green, text=BIG)
    calls = {"n": 0}
    real = bulk.ImportRow.objects.bulk_create

    def flaky(objs, *a, **k):
        calls["n"] += 1
        if calls["n"] == 3:
            raise RuntimeError("crash")
        return real(objs, *a, **k)

    monkeypatch.setattr(bulk.ImportRow.objects, "bulk_create", flaky)
    with pytest.raises(RuntimeError):
        bulk.stage(b)
    b.refresh_from_db()
    assert b.staged_through == 200
    monkeypatch.setattr(bulk.ImportRow.objects, "bulk_create", real)
    bulk.stage(b)
    assert ImportRow.objects.filter(batch=b).count() == 250


def test_individual_list_types_are_all_held(tree, surgical, users, green):
    surgical.settings.is_individual = True
    surgical.settings.save()
    b = batch(tree, surgical, users, green, text=BIG)
    assert bulk.stage(b)["held"] == 250


def test_sample_size_formula():
    assert bulk.sample_size(50) == 50 and bulk.sample_size(10_000_000) == 385
