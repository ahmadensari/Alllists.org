from datetime import timedelta

from django.core.management import call_command

from core import clock, jobs
from core.models import AuditLog, JobRun


def test_due_jobs_run_once_per_interval_and_record_results(db):
    first = jobs.run_due()
    assert set(first) == set(jobs.JOBS) and all(not v.startswith("RuntimeError") for v in first.values())
    assert jobs.run_due() == {}  # nothing is due a moment later
    later = clock.now() + timedelta(hours=2)
    assert set(jobs.run_due(now=later)) == {"expiry_sweeper", "placement_expiry"}  # only the hourly job
    assert set(jobs.run_due(now=clock.now() + timedelta(days=2))) >= {
        "rollup_recount",
        "hold_release",
        "audit_chain_verify",
    }


def test_a_failing_job_is_recorded_and_does_not_stop_the_others(db, monkeypatch):
    def boom():
        raise RuntimeError("disk full")

    monkeypatch.setitem(jobs.JOBS, "expiry_sweeper", (jobs.HOUR, boom))
    ran = jobs.run_due()
    assert ran["expiry_sweeper"].startswith("RuntimeError: disk full") and "rollup_recount" in ran
    assert JobRun.objects.get(name="expiry_sweeper").last_error


def test_a_broken_audit_chain_is_reported_by_the_job(pg, db):
    from django.db import connection
    from core.models import audit

    audit("t.one")
    row = audit("t.two")
    with connection.cursor() as cur:
        cur.execute("ALTER TABLE core_auditlog DISABLE TRIGGER core_auditlog_append_only")
        cur.execute("UPDATE core_auditlog SET action = 'tampered' WHERE id = %s", [row.id])
        cur.execute("ALTER TABLE core_auditlog ENABLE TRIGGER core_auditlog_append_only")
    ran = jobs.run_due(only=["audit_chain_verify"])
    assert "audit chain broken" in ran["audit_chain_verify"]
    assert AuditLog.objects.filter(action="audit.chain_broken").exists()


def test_command_runs_the_jobs(db, capsys):
    call_command("run_scheduled", "--only", "expiry_sweeper")
    assert "expiry_sweeper" in capsys.readouterr().out
