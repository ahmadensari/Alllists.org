"""Agent pipeline (plan 7.6, rules R35, R22, R07, R08). Short capped jobs, one record at a time; evidence must be quoted
verbatim; the agent can only write drafts; a kill switch and day and month caps stop spending."""

import re
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Sum

from core import clock
from core.models import audit, flag_enabled
from core.textfold import fold
from entries import services as es
from intake.gate import SourceBlocked, assert_allowed

from .fetcher import FetchRefused
from .models import AgentJob, DraftEntry

CHECKED_FIELDS = ("name", "phone", "address")


class AgentStopped(Exception):
    pass


def norm_space(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def digits(text):
    return re.sub(r"\D", "", text or "")


def quoted_verbatim(field, value, page_text):
    """A phone or address (or name) counts as evidence only if it appears in the fetched page, word for word. A phone is
    compared by its digits so spacing differences do not matter."""
    if not value:
        return False
    if field == "phone":
        d = digits(value)
        return len(d) >= 7 and d in digits(page_text)
    return norm_space(value) in norm_space(page_text)


# ---- caps and kill switch ---------------------------------------------------------------------------------------


def kill_switch_on():
    return bool(getattr(settings, "AI_KILL_SWITCH", False)) or flag_enabled("agent_kill_switch")


def spent_since(since):
    return AgentJob.objects.filter(started_at__gte=since).aggregate(s=Sum("spent_minor"))["s"] or 0


def cap_status(now=None):
    """Spending against the day and month caps, and the 50 and 80 percent warning lines."""
    now = now or clock.now()
    day = spent_since(now.replace(hour=0, minute=0, second=0, microsecond=0))
    month = spent_since(now.replace(day=1, hour=0, minute=0, second=0, microsecond=0))
    dcap, mcap = settings.AI_DAILY_CAP_MINOR, settings.AI_MONTHLY_CAP_MINOR
    return {
        "day": day,
        "day_cap": dcap,
        "month": month,
        "month_cap": mcap,
        "day_pct": round(100 * day / dcap) if dcap else 0,
        "month_pct": round(100 * month / mcap) if mcap else 0,
        "blocked": bool((dcap and day >= dcap) or (mcap and month >= mcap)),
    }


def _warn(now):
    st = cap_status(now)
    for key in ("day", "month"):
        for line in (50, 80):
            if st[f"{key}_pct"] >= line:
                audit("ai.cap_warning", object_type="ai_budget", object_uid=f"{key}:{line}", payload=st)


def start_job(kind, source, *, budget_minor=None):
    """Create a job after checking the licence gate, the kill switch and the caps. Caps must be configured to start."""
    if not settings.AI_DAILY_CAP_MINOR or not settings.AI_MONTHLY_CAP_MINOR:
        raise AgentStopped("set AI_DAILY_CAP_MINOR and AI_MONTHLY_CAP_MINOR before running agents")
    if kill_switch_on():
        raise AgentStopped("the AI kill switch is on")
    if cap_status()["blocked"]:
        raise AgentStopped("the day or month budget is used up")
    assert_allowed(source, "agent_fetch")
    return AgentJob.objects.create(
        kind=kind,
        source=source,
        budget_cap_minor=budget_minor or settings.AI_JOB_CAP_MINOR,
        status=AgentJob.Status.RUNNING,
    )


def _stop(job, reason):
    job.status, job.stop_reason, job.finished_at = AgentJob.Status.STOPPED, reason[:120], clock.now()
    job.save()
    audit("ai.job_stopped", object_type="agent_job", object_uid=str(job.pk), payload={"reason": reason})


def _finish(job):
    job.status, job.finished_at = AgentJob.Status.DONE, clock.now()
    job.save()
    _warn(clock.now())


# ---- drafting ----------------------------------------------------------------------------------------------------


def run_draft_job(job, urls, fetcher, model):
    """Fetch each page, extract, reject anything not quoted verbatim, stage the rest. Stops at the first refusal."""
    job.model = getattr(model, "name", "")
    for url in urls:
        if kill_switch_on():
            return _stop(job, "kill switch")
        if job.spent_minor >= job.budget_cap_minor or cap_status()["blocked"]:
            return _stop(job, "budget used up")
        try:
            page = fetcher.get(url)
        except FetchRefused as exc:
            return _stop(job, f"source refused: {exc}")
        ex = model.extract(page.text)
        job.spent_minor += ex.cost_minor
        job.tokens_in += ex.tokens_in
        job.tokens_out += ex.tokens_out
        job.save()
        fields = {
            k: v for k, v in ex.fields.items() if k in ("name", "phone", "address", "website")
        }  # unknown keys dropped
        quotes = {k: v for k, v in fields.items() if k in CHECKED_FIELDS and quoted_verbatim(k, v, page.text)}
        missing = [k for k in ("name", "phone") if k not in quotes]
        state, reason = DraftEntry.State.STAGED, ""
        if missing:
            state, reason = DraftEntry.State.REJECTED, f"not quoted from the page: {', '.join(missing)}"
        DraftEntry.objects.create(
            job=job,
            raw=fields,
            evidence_quotes=quotes,
            source_urls=[url],
            confidence=ex.confidence,
            cost_minor=ex.cost_minor,
            state=state,
            reason=reason,
        )
    _finish(job)


@transaction.atomic
def promote(draft, *, place, concept, actor=None):
    """Turn a staged draft into a draft entry. It stays hidden and earns nothing (rules R08, R09); a person or a second
    source must check it."""
    if draft.state != DraftEntry.State.STAGED:
        raise es.EntryError("only staged drafts can be promoted")
    try:
        assert_allowed(draft.job.source, "import")
    except SourceBlocked:
        assert_allowed(draft.job.source, "agent_fetch")
    raw = draft.raw
    contacts = [("phone", raw["phone"])] if raw.get("phone") else []
    entry = es.create_entry(
        name=raw["name"],
        place=place,
        primary_concept=concept,
        created_via="agent",
        source=draft.job.source,
        address_text=raw.get("address", ""),
        website=raw.get("website", "") if raw.get("website", "").startswith("http") else "",
        contacts=contacts,
    )
    draft.state, draft.entry = DraftEntry.State.PROMOTED, entry
    draft.save(update_fields=["state", "entry"])
    audit("ai.promote", actor=actor, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return entry


# ---- second check (rule R07: a different source) -----------------------------------------------------------------------


def run_second_check(entry, source, url, fetcher, model):
    """Compare an entry with a page from a different source. Matching name and phone records an AI check; anything else
    records nothing. Returns True when a check was recorded."""
    job = start_job(AgentJob.Kind.SECOND_CHECK, source)
    job.model = getattr(model, "name", "")
    try:
        page = fetcher.get(url)
    except FetchRefused as exc:
        _stop(job, f"source refused: {exc}")
        return False
    ex = model.extract(page.text)
    job.spent_minor += ex.cost_minor
    job.save()
    f = ex.fields
    phones = [c.value_enc for c in entry.contact_set.filter(kind__in=["phone", "mobile", "whatsapp"])]
    name_ok = quoted_verbatim("name", f.get("name"), page.text) and fold(f["name"]) == entry.name_fold
    phone_ok = quoted_verbatim("phone", f.get("phone"), page.text) and any(
        digits(p)[-9:] == digits(f["phone"])[-9:] for p in phones
    )
    _finish(job)
    if not (name_ok and phone_ok):
        return False
    es.record_verification(
        entry,
        field_group="identity",
        level="ai",
        source=source,
        method="web page",
        evidence=f"Page {url} shows name '{f.get('name')}' and phone '{f.get('phone')}'",
    )
    return True


# ---- reporting -----------------------------------------------------------------------------------------------------------


def cost_per_verified(days=30):
    """Agent spend divided by drafts that reached a person's check; the plan stops a job kind above 30 cents."""
    since = clock.now() - timedelta(days=days)
    spend = AgentJob.objects.filter(started_at__gte=since).aggregate(s=Sum("spent_minor"))["s"] or 0
    verified = (
        DraftEntry.objects.filter(
            created_at__gte=since, state="promoted", entry__verification_current__level__in=["surveyor", "owner"]
        )
        .distinct()
        .count()
    )
    return {"spend_minor": spend, "verified": verified, "per_verified_minor": (spend / verified) if verified else None}
