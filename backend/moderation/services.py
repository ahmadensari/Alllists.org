"""Reports, suggestions, takedown and erasure (plan 15). Facts are corrected, never opinions added."""

from datetime import timedelta

from django.db import transaction

from core import clock
from core.crypto import encrypt, keyed_hash
from core.models import audit
from entries import services as es
from entries.models import Entry, NameVariant, Social

from .models import Report, SuggestedEdit, Takedown

MAX_REPORTS_PER_DAY = 10
ERASURE_DAYS = 30


class ModerationError(ValueError):
    pass


def address_hash(address):
    return keyed_hash(f"addr:{address}") if address else ""


@transaction.atomic
def submit_report(entry, kind, text="", *, address="", contact=""):
    """Anyone may report. Rate-limited by a keyed hash of the address; a removal request also opens a takedown."""
    if kind not in Report.Kind.values or kind == Report.Kind.CLAIM_DISPUTE and not text:
        raise ModerationError("unknown report type")
    h = address_hash(address)
    if (
        h
        and Report.objects.filter(reporter_hash=h, created_at__gte=clock.now() - timedelta(days=1)).count()
        >= MAX_REPORTS_PER_DAY
    ):
        raise ModerationError("too many reports today")
    report = Report.objects.create(
        entry=entry,
        kind=kind,
        text=text[:2000],
        reporter_hash=h,
        reporter_contact_enc=encrypt(contact.strip()) if contact.strip() else "",
    )
    if kind == Report.Kind.REMOVE_MY_DATA:
        Takedown.objects.create(
            entry=entry,
            requester_hash=h,
            kind="erasure",
            legal_basis="data subject request",
            due_at=clock.now() + timedelta(days=ERASURE_DAYS),
            log=[{"ts": clock.now().isoformat(), "event": "opened"}],
        )
    audit(
        "report.submit",
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"kind": kind},
    )
    return report


@transaction.atomic
def decide_report(report, *, actor, uphold, resolution=""):
    if report.state in (Report.State.UPHELD, Report.State.REJECTED):
        raise ModerationError("already decided")
    report.state = Report.State.UPHELD if uphold else Report.State.REJECTED
    report.resolution, report.decided_at, report.assigned_to = resolution[:300], clock.now(), actor
    report.save()
    entry = report.entry
    if uphold:
        if report.kind == Report.Kind.CLOSED:
            es.update_entry(entry, actor=actor, status=Entry.Status.PERM_CLOSED)
        elif report.kind == Report.Kind.FAKE:
            entry.publish_state = Entry.PublishState.SUPPRESSED
            entry.save(update_fields=["publish_state"])
    audit(
        "report.decide",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"kind": report.kind, "upheld": uphold},
    )
    return report


@transaction.atomic
def suggest_edit(entry, field_key, value, actor=None):
    if field_key not in es.EDITABLE or field_key in ("place", "addons"):
        raise ModerationError("that field cannot be edited by suggestion")
    return SuggestedEdit.objects.create(entry=entry, field_key=field_key, new_value=value, actor=actor)


@transaction.atomic
def decide_suggestion(suggestion, *, actor, accept):
    if suggestion.state != SuggestedEdit.State.PENDING:
        raise ModerationError("already decided")
    suggestion.state = SuggestedEdit.State.ACCEPTED if accept else SuggestedEdit.State.REJECTED
    suggestion.decided_by_id = actor.pk
    suggestion.save()
    if accept:
        es.update_entry(suggestion.entry, actor=actor, **{suggestion.field_key: suggestion.new_value})
    return suggestion


@transaction.atomic
def execute_erasure(takedown, *, actor):
    """Tombstone an entry: personal fields replaced, contacts removed, hashes suppressed so a re-import cannot return it."""
    from outreach.services import suppress

    entry = takedown.entry
    if entry is None:
        raise ModerationError("nothing to erase")
    for c in list(entry.contact_set.all()):
        suppress(c.value_hash, "", "erasure")
    suppress(keyed_hash(f"entry-name:{entry.country_code}:{entry.name_fold}"), "", "erasure")
    entry.contact_set.all().delete()
    Social.objects.filter(entry=entry).delete()
    NameVariant.objects.filter(entry=entry).delete()
    entry.name, entry.name_fold = "Removed at the owner's request", ""
    entry.description = entry.address_text = entry.website = ""
    entry.address, entry.addons = {}, {}
    entry.lat = entry.lon = None
    entry.publish_state = Entry.PublishState.TOMBSTONED
    entry.deleted_at, entry.tombstone_reason = clock.now(), "erasure"
    entry.save()
    takedown.state, takedown.done_at = Takedown.State.DONE, clock.now()
    takedown.log = list(takedown.log) + [{"ts": clock.now().isoformat(), "event": "erased", "by": actor.pk}]
    takedown.save()
    audit("takedown.erase", actor=actor, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return takedown


@transaction.atomic
def refuse_takedown(takedown, *, actor, reason):
    takedown.state = Takedown.State.REFUSED
    takedown.log = list(takedown.log) + [
        {"ts": clock.now().isoformat(), "event": "refused", "reason": reason[:200], "by": actor.pk}
    ]
    takedown.save()
    audit("takedown.refuse", actor=actor, object_type="takedown", object_uid=str(takedown.pk))
