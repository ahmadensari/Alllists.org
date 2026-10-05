"""Staff console (plan 15.1): queue screens for the real work. Django admin stays for raw inspection and seeding.
Every action checks a capability, runs through a service, and is audited there."""

from dataclasses import dataclass
from typing import Callable

from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from accounts.roles import has_cap
from core.models import AuditLog, CountrySwitch, audit, verify_audit_chain
from entries import services as es
from entries.models import Claim
from intake.models import DedupeCandidate, ImportBatch, Source
from moderation import services as mod
from moderation.models import Report, SuggestedEdit, Takedown
from outreach.models import OutboxMessage
from places import services as ps
from places.models import PlaceProposal
from volunteers import services as vs
from volunteers.models import Task


@dataclass
class Queue:
    key: str
    title: str
    cap: str
    items: Callable
    actions: tuple  # (action key, label)
    describe: Callable


def _entry_line(e):
    return f"{e.name} ({e.place_path})"


QUEUES = {}


def queue(**kw):
    q = Queue(**kw)
    QUEUES[q.key] = q
    return q


queue(
    key="dedupe",
    title="Possible duplicates",
    cap="moderate",
    actions=(("merge", "Merge"), ("reject", "Not a duplicate")),
    items=lambda: DedupeCandidate.objects.filter(state="pending")
    .select_related("a_entry", "b_entry")
    .order_by("-score")[:100],
    describe=lambda c: f"{c.a_entry.name} / {c.b_entry.name} (score {c.score:.2f})",
)
queue(
    key="areas",
    title="Area proposals",
    cap="moderate",
    actions=(("approve", "Approve"), ("reject", "Reject")),
    items=lambda: PlaceProposal.objects.filter(state="pending").select_related("parent")[:100],
    describe=lambda p: f"{p.proposed_name} under {p.parent.path}",
)
queue(
    key="claims",
    title="Claims to review",
    cap="claim_decide",
    actions=(("approve", "Approve"), ("reject", "Reject")),
    items=lambda: Claim.objects.filter(state="pending").select_related("entry", "user")[:100],
    describe=lambda c: f"{c.entry.name} claimed by {c.user.username} ({c.method}): {c.evidence_text[:120]}",
)
queue(
    key="reports",
    title="Reports",
    cap="moderate",
    actions=(("uphold", "Uphold"), ("reject", "Reject")),
    items=lambda: Report.objects.filter(state__in=["open", "assigned"])
    .select_related("entry")
    .order_by("created_at")[:100],
    describe=lambda r: f"{r.entry.name}: {r.kind} {r.text[:120]}",
)
queue(
    key="suggestions",
    title="Suggested edits",
    cap="moderate",
    actions=(("accept", "Accept"), ("reject", "Reject")),
    items=lambda: SuggestedEdit.objects.filter(state="pending").select_related("entry")[:100],
    describe=lambda s: f"{s.entry.name}: {s.field_key} -> {s.new_value}",
)
queue(
    key="takedowns",
    title="Removal and erasure requests",
    cap="takedown",
    actions=(("erase", "Erase"), ("refuse", "Refuse")),
    items=lambda: Takedown.objects.filter(state="open").select_related("entry").order_by("due_at")[:100],
    describe=lambda t: f"{t.entry.uid if t.entry else '-'} {t.kind} due {t.due_at:%j %b %Y}" if t.due_at else str(t.pk),
)


def _gate(request, cap):
    if not has_cap(request.user, cap):
        return HttpResponseForbidden("Not allowed")
    return None


def index(request):
    rows = []
    for q in QUEUES.values():
        if has_cap(request.user, q.cap):
            rows.append({"q": q, "n": len(list(q.items()))})
    extra = [
        ("imports", "Import batches", "moderate"),
        ("sources", "Source register", "moderate"),
        ("tasks", "Verification tasks", "verify"),
        ("audit", "Audit log", "view_audit"),
        ("switches", "Country switches", "edit_registries"),
        ("outbox", "Outbox", "moderate"),
    ]
    return render(
        request,
        "catalog/staff/index.html",
        {
            "rows": rows,
            "extra": [e for e in extra if has_cap(request.user, e[2])],
            "robots": "noindex,nofollow",
            "title": "Staff",
        },
    )


def show_queue(request, key):
    q = QUEUES.get(key)
    if q is None:
        raise Http404
    denied = _gate(request, q.cap)
    if denied:
        return denied
    items = [{"obj": o, "text": q.describe(o)} for o in q.items()]
    return render(
        request, "catalog/staff/queue.html", {"q": q, "items": items, "robots": "noindex,nofollow", "title": q.title}
    )


@require_POST
def act(request, key, pk, action):
    q = QUEUES.get(key)
    if q is None or action not in dict(q.actions):
        raise Http404
    denied = _gate(request, q.cap)
    if denied:
        return denied
    obj = (
        {
            "dedupe": DedupeCandidate,
            "areas": PlaceProposal,
            "claims": Claim,
            "reports": Report,
            "suggestions": SuggestedEdit,
            "takedowns": Takedown,
        }[key]
        .objects.filter(pk=pk)
        .first()
    )
    if obj is None:
        raise Http404
    actor, note = request.user, request.POST.get("note", "")
    try:
        if key == "dedupe":
            if action == "merge":
                keep, drop = sorted([obj.a_entry, obj.b_entry], key=lambda e: e.created_at)
                es.merge_entries(keep, drop, actor=actor, score=obj.score)
                obj.state = "merged"
            else:
                obj.state = "rejected"
            obj.decided_by_id = actor.pk
            obj.save()
        elif key == "areas":
            if action == "approve":
                ps.approve_proposal(obj, actor=actor)
            else:
                obj.state, obj.decided_by = "rejected", actor.pk
                obj.save()
        elif key == "claims":
            es.decide_claim(obj, actor=actor, approve=action == "approve")
        elif key == "reports":
            mod.decide_report(obj, actor=actor, uphold=action == "uphold", resolution=note)
        elif key == "suggestions":
            mod.decide_suggestion(obj, actor=actor, accept=action == "accept")
        elif key == "takedowns":
            (
                mod.execute_erasure(obj, actor=actor)
                if action == "erase"
                else mod.refuse_takedown(obj, actor=actor, reason=note or "refused")
            )
    except (es.EntryError, mod.ModerationError, ps.PlaceError) as exc:
        messages.error(request, str(exc))
    return redirect(f"/staff/{key}/")


def imports(request):
    denied = _gate(request, "moderate")
    return denied or render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Import batches",
            "head": ["Batch", "Source", "Status", "Counts"],
            "rows": [
                [b.pk, b.source.name, b.status, b.counts]
                for b in ImportBatch.objects.select_related("source").order_by("-id")[:100]
            ],
            "robots": "noindex,nofollow",
        },
    )


def sources(request):
    denied = _gate(request, "moderate")
    return denied or render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Source register",
            "head": ["Name", "Tier", "Status", "Reviewed", "Bulk allowed"],
            "rows": [
                [s.name, s.tier, s.status, s.reviewed_on or "never", s.bulk_permission]
                for s in Source.objects.order_by("tier", "name")
            ],
            "robots": "noindex,nofollow",
        },
    )


def tasks(request):
    denied = _gate(request, "verify")
    if denied:
        return denied
    if request.method == "POST" and request.POST.get("action") == "queue":
        n = vs.queue_unchecked()
        messages.success(request, f"{n} tasks created")
        return redirect("/staff/tasks/")
    rows = [
        [t.pk, t.entry.name if t.entry else "-", t.state, t.assigned_to or "-", t.minutes or ""]
        for t in Task.objects.select_related("entry", "assigned_to").order_by("-id")[:100]
    ]
    rate = vs.completion_rate()
    return render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Verification tasks",
            "head": ["Task", "Entry", "State", "Assigned", "Minutes"],
            "rows": rows,
            "note": f"Completion rate (14 days): {'n/a' if rate is None else f'{rate:.0%}'}",
            "post_action": ("queue", "Queue tasks for unchecked entries"),
            "robots": "noindex,nofollow",
        },
    )


def audit_view(request):
    denied = _gate(request, "view_audit")
    if denied:
        return denied
    broken = verify_audit_chain()
    rows = [
        [a.id, a.ts.strftime("%Y-%m-%d %H:%M"), a.action, a.object_type, a.object_uid, a.actor_id or "-"]
        for a in AuditLog.objects.order_by("-id")[:200]
    ]
    return render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Audit log",
            "head": ["#", "Time", "Action", "Object", "Uid", "Actor"],
            "rows": rows,
            "note": "Hash chain intact" if broken is None else f"CHAIN BROKEN at row {broken}",
            "robots": "noindex,nofollow",
        },
    )


def switches(request):
    denied = _gate(request, "edit_registries")
    if denied:
        return denied
    fields = [
        "browsing_on",
        "indexing_on",
        "selling_on",
        "outreach_on",
        "ads_on",
        "named_individuals_on",
        "health_prices_on",
        "child_services_on",
    ]
    if request.method == "POST":
        sw, _ = CountrySwitch.objects.get_or_create(country_code=request.POST.get("country", "").upper()[:2])
        field = request.POST.get("field")
        if field in fields:
            setattr(sw, field, request.POST.get("value") == "on")
            sw.cleared_by, sw.legal_note = request.user.username, request.POST.get("note", sw.legal_note)[:300]
            sw.save()
            audit(
                "switch.change",
                actor=request.user,
                object_type="country_switch",
                object_uid=sw.country_code,
                payload={field: sw.__dict__[field]},
            )
        return redirect("/staff/switches/")
    return render(
        request,
        "catalog/staff/switches.html",
        {
            "switches": CountrySwitch.objects.order_by("country_code"),
            "fields": fields,
            "robots": "noindex,nofollow",
            "title": "Country switches",
        },
    )


def outbox(request):
    denied = _gate(request, "moderate")
    return denied or render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Outbox (never shows recipients)",
            "head": ["#", "Channel", "Kind", "State", "Created"],
            "rows": [
                [m.pk, m.channel, m.kind, m.state, m.created_at.strftime("%Y-%m-%d %H:%M")]
                for m in OutboxMessage.objects.order_by("-id")[:100]
            ],
            "robots": "noindex,nofollow",
        },
    )
