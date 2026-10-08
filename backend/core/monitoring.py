"""Health checks behind the staff metrics page and the hourly alert job (plan 18.3, P3.15, P3.20).

Each check returns a Metric with state ok, warn or alert and a plain sentence. Nothing here changes data."""

from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.db import connection

from . import clock
from .models import JobRun, OpsRecord, verify_audit_chain

OK, WARN, ALERT = "ok", "warn", "alert"


@dataclass
class Metric:
    area: str
    name: str
    value: str
    state: str
    note: str = ""


def _rate_state(rate, alert_at, warn_at=None):
    if rate is None:
        return OK
    if rate > alert_at:
        return ALERT
    if warn_at is not None and rate > warn_at:
        return WARN
    return OK


def jobs():
    from .jobs import JOBS

    out, now = [], clock.now()
    rows = {r.name: r for r in JobRun.objects.all()}
    failing = [n for n, r in rows.items() if r.last_error]
    overdue = [
        n for n, (every, _) in JOBS.items() if n in rows and rows[n].last_run and now - rows[n].last_run > every * 3
    ]
    never = [n for n in JOBS if n not in rows or not rows[n].last_run]
    out.append(Metric("Jobs", "failing jobs", str(len(failing)), ALERT if failing else OK, ", ".join(failing)))
    out.append(Metric("Jobs", "overdue jobs", str(len(overdue)), ALERT if overdue else OK, ", ".join(overdue)))
    out.append(Metric("Jobs", "never run", str(len(never)), WARN if never else OK, ", ".join(never)))
    return out


def audit_chain():
    broken = verify_audit_chain()
    return [
        Metric(
            "Integrity",
            "audit chain",
            "intact" if broken is None else f"broken at {broken}",
            OK if broken is None else ALERT,
        )
    ]


def data_quality():
    from entries.models import VerificationCurrent
    from intake.models import DedupeCandidate

    out, now = [], clock.now()
    total = VerificationCurrent.objects.filter(state="verified").count()
    expired = VerificationCurrent.objects.filter(state="verified", expires_at__lt=now).count()
    share = (expired / total) if total else None
    out.append(
        Metric(
            "Data quality",
            "expired checks share",
            "n/a" if share is None else f"{share:.0%}",
            _rate_state(share, 0.25),
            "alert above 25%",
        )
    )
    merged = DedupeCandidate.objects.filter(state="merged").count()
    rejected = DedupeCandidate.objects.filter(state="rejected").count()
    rr = (rejected / (merged + rejected)) if merged + rejected else None
    out.append(
        Metric(
            "Data quality",
            "duplicate rejection rate",
            "n/a" if rr is None else f"{rr:.0%}",
            _rate_state(rr, 0.10),
            "reviewers reject more than 10% of merges",
        )
    )
    from volunteers.models import ContributorProfile

    low = ContributorProfile.objects.filter(accuracy__lt=0.8).count()
    out.append(Metric("Data quality", "surveyors under 80% accuracy", str(low), WARN if low else OK))
    return out


def search():
    from analytics.models import Event

    since = clock.now() - timedelta(days=7)
    q = Event.objects.filter(name="search", ts__gte=since).count()
    z = Event.objects.filter(name="search_zero_result", ts__gte=since).count()
    rate = (z / (q + z)) if q + z >= 50 else None
    return [
        Metric(
            "Search",
            "zero-result rate (7 days)",
            "n/a" if rate is None else f"{rate:.0%}",
            _rate_state(rate, 0.15),
            "alert above 15%",
        )
    ]


def ai_spend():
    from agents import services as ag

    st = ag.cap_status()
    state = OK
    for pct in (st["day_pct"], st["month_pct"]):
        state = ALERT if pct >= 80 else WARN if pct >= 50 and state != ALERT else state
    kill = ag.kill_switch_on()
    return [
        Metric(
            "AI",
            "day and month spend",
            f"{st['day_pct']}% / {st['month_pct']}%",
            state,
            "warn at 50%, alert at 80% of the caps",
        ),
        Metric("AI", "kill switch", "ON" if kill else "off", WARN if kill else OK),
    ]


def outreach():
    from outreach.models import Campaign

    paused = Campaign.objects.filter(status="paused").count()
    return [
        Metric(
            "Outreach",
            "paused campaigns",
            str(paused),
            ALERT if paused else OK,
            "auto-paused above 2% opt-out or 10% failures",
        )
    ]


def money():
    from billing.reconcile import all_ok, reconcile

    res = reconcile()
    bad = [r["check"] for r in res if not r["ok"]]
    return [
        Metric(
            "Money",
            "ledger reconciliation",
            "agrees" if all_ok(res) else f"{len(bad)} differ",
            OK if not bad else ALERT,
            "; ".join(bad),
        )
    ]


def abuse():
    from access.models import QuotaCounter

    heavy = QuotaCounter.objects.filter(key="fragments", day=clock.today(), count__gte=500).count()
    return [Metric("Abuse", "addresses over 500 fragment loads today", str(heavy), WARN if heavy else OK)]


def database():
    with connection.cursor() as cur:
        if connection.vendor != "postgresql":
            return [Metric("Database", "engine", connection.vendor, WARN, "production runs PostgreSQL")]
        cur.execute("select count(*) from pg_stat_activity where datname = current_database()")
        conns = cur.fetchone()[0]
        cur.execute("select pg_database_size(current_database())")
        size = cur.fetchone()[0]
        cur.execute(
            "select coalesce(extract(epoch from max(now() - xact_start)), 0) from pg_stat_activity "
            "where datname = current_database() and state <> 'idle' and xact_start is not null"
        )
        longest = cur.fetchone()[0]
    return [
        Metric("Database", "connections", str(conns), WARN if conns > 80 else OK),
        Metric("Database", "size", f"{size / 1e6:.1f} MB", OK),
        Metric("Database", "longest open transaction", f"{longest:.0f} s", WARN if longest > 300 else OK),
    ]


def backups():
    now = clock.now()
    last = OpsRecord.objects.filter(kind="backup").order_by("-at").first()
    drill = OpsRecord.objects.filter(kind="restore_drill").order_by("-at").first()
    out = []
    age = (now - last.at) if last else None
    out.append(
        Metric(
            "Backups",
            "last backup",
            "never" if last is None else f"{age.days}d ago",
            ALERT if last is None or age > timedelta(days=2) else OK,
            "nightly dump expected",
        )
    )
    dage = (now - drill.at) if drill else None
    out.append(
        Metric(
            "Backups",
            "last restore drill",
            "never" if drill is None else f"{dage.days}d ago",
            ALERT if drill is None or dage > timedelta(days=100) else OK,
            "a drill that is skipped is an alert",
        )
    )
    return out


CHECKS = [jobs, audit_chain, data_quality, search, ai_spend, outreach, money, abuse, database, backups]


def collect():
    out = []
    for fn in CHECKS:
        try:
            out.extend(fn())
        except Exception as exc:  # one broken check must not hide the rest; it is itself an alert
            out.append(Metric("Monitor", fn.__name__, type(exc).__name__, ALERT, str(exc)[:200]))
    return out


def alerts(metrics=None):
    return [m for m in (metrics or collect()) if m.state == ALERT]


def send_alerts(now=None):
    """Email each distinct alert to ALERT_EMAILS at most once a day. Returns how many were sent."""
    from django.core.mail import send_mail

    now = now or clock.now()
    to = list(getattr(settings, "ALERT_EMAILS", []))
    sent = 0
    for m in alerts():
        key = f"{m.area}:{m.name}"
        if OpsRecord.objects.filter(kind="alert_sent", key=key, at__gte=now - timedelta(days=1)).exists():
            continue
        if to:
            send_mail(f"AllLists alert: {m.name}", f"{m.area} / {m.name}: {m.value}. {m.note}", None, to)
        OpsRecord.objects.create(kind="alert_sent", key=key, detail=f"{m.value} {m.note}"[:300], at=now)
        sent += 1
    return sent
