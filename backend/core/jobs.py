"""Scheduled jobs (plan appendix F). `run_due()` runs whatever is due and records the result; a failing job never stops
the others. Run it from cron or a loop: `python manage.py run_scheduled`."""

from datetime import timedelta

from . import clock
from .models import JobRun, audit, verify_audit_chain

HOUR, DAY, WEEK = timedelta(hours=1), timedelta(days=1), timedelta(days=7)


def _rollups():
    from analytics.rollups import recount_all

    return f"{recount_all()} cells"


def _expiry():
    from entries.services import sweep_expired

    return str(sweep_expired())


def _stewards():
    from entries.services import expire_stewards

    return f"{expire_stewards()} expired"


def _holds():
    from ledger.services import release_holds

    return f"{release_holds()} released"


def _chain():
    broken = verify_audit_chain()
    if broken is not None:
        audit("audit.chain_broken", object_type="audit_log", object_uid=str(broken))
        raise RuntimeError(f"audit chain broken at row {broken}")
    return "intact"


def _reconcile():
    from billing.reconcile import all_ok, reconcile

    results = reconcile()
    if not all_ok(results):
        bad = [r["check"] for r in results if not r["ok"]]
        audit("ledger.reconcile_failed", object_type="ledger", object_uid="USD", payload={"checks": bad})
        raise RuntimeError("ledger does not reconcile: " + "; ".join(bad))
    return "agrees"


def _alerts():
    from .monitoring import send_alerts

    return f"{send_alerts()} alerts sent"


def _unchecked():
    from volunteers.services import queue_unchecked

    return f"{queue_unchecked()} tasks"


def _quota_cleanup():
    from access.models import QuotaCounter

    n, _ = QuotaCounter.objects.filter(day__lt=clock.today() - timedelta(days=7)).delete()
    return f"{n} counters"


def _retention():
    from analytics.models import Event
    from outreach.models import OutboxMessage

    cut = clock.now() - timedelta(days=365)
    a, _ = Event.objects.filter(ts__lt=cut).delete()
    b, _ = OutboxMessage.objects.filter(created_at__lt=cut, state__in=["sent", "failed"]).delete()
    return f"{a} events, {b} messages"


def _placements():
    from access.placements import expire_due

    return f"{expire_due()} ended"


JOBS = {
    "placement_expiry": (HOUR, _placements),
    "rollup_recount": (DAY, _rollups),
    "expiry_sweeper": (HOUR, _expiry),
    "steward_inactivity": (DAY, _stewards),
    "hold_release": (DAY, _holds),
    "audit_chain_verify": (DAY, _chain),
    "ledger_reconcile": (DAY, _reconcile),
    "ops_alerts": (HOUR, _alerts),
    "queue_unchecked": (DAY, _unchecked),
    "quota_cleanup": (DAY, _quota_cleanup),
    "retention_purge": (WEEK, _retention),
}


def run_due(now=None, only=None):
    now = now or clock.now()
    ran = {}
    for name, (every, fn) in JOBS.items():
        if only and name not in only:
            continue
        row, _ = JobRun.objects.get_or_create(name=name)
        if row.last_run and now - row.last_run < every:
            continue
        try:
            row.last_result, row.last_error = str(fn())[:200], ""
        except Exception as exc:  # one failing job must not stop the rest
            row.last_result, row.last_error = "", f"{type(exc).__name__}: {exc}"[:300]
        row.last_run = now
        row.save()
        ran[name] = row.last_error or row.last_result
    return ran
