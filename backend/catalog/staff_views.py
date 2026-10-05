"""Staff console (plan 15.1): queue screens for the real work. Django admin stays for raw inspection and seeding.
Every action checks a capability, runs through a service, and is audited there."""

from dataclasses import dataclass
from typing import Callable

from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from access import placements as pl
from access.models import Ad
from accounts.roles import has_cap
from core.models import AuditLog, CountrySwitch, audit, verify_audit_chain
from entries import services as es
from entries.models import Claim, CompanySection
from intake.models import DedupeCandidate, ImportBatch, Source
from moderation import services as mod
from moderation.models import Report, SuggestedEdit, Takedown
from outreach import campaigns
from outreach.models import Campaign, MessageTemplate, OutboxMessage, SupplierVerification
from ledger import services as ledger_services
from ledger.models import PayoutBatch, PayoutProfile
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
    key="company",
    title="Company page text",
    cap="moderate",
    actions=(("approve", "Approve"), ("reject", "Reject")),
    items=lambda: CompanySection.objects.filter(state="pending").select_related("entry").order_by("updated_at")[:100],
    describe=lambda s: f"{s.entry.name} / {s.kind}: {s.body[:160]}",
)
queue(
    key="suppliers",
    title="Supplier verification",
    cap="moderate",
    actions=(("approve", "Verify"), ("reject", "Reject")),
    items=lambda: SupplierVerification.objects.filter(state="pending").select_related("user")[:100],
    describe=lambda s: f"{s.company} ({s.user.username})",
)
queue(
    key="templates",
    title="Message templates to approve",
    cap="moderate",
    actions=(("approve", "Approve"),),
    items=lambda: MessageTemplate.objects.filter(provider_state="submitted")[:100],
    describe=lambda t: f"{t.key} / {t.channel} / {t.language}: {t.body[:140]}",
)
queue(
    key="campaigns",
    title="Campaigns to approve",
    cap="moderate",
    actions=(("approve", "Approve"),),
    items=lambda: Campaign.objects.filter(status="pending").select_related("buyer", "concept")[:100],
    describe=lambda c: f"{c.buyer.username}: {c.channel} to {c.scope_path or 'world'} ({c.budget_minor} budget)",
)
queue(
    key="ads",
    title="Text ads to approve",
    cap="moderate",
    actions=(("approve", "Approve"), ("reject", "Reject")),
    items=lambda: Ad.objects.filter(state="pending").exclude(order_ref="").select_related("entry")[:100],
    describe=lambda a: f"{a.headline} / {a.body[:80]} -> {a.entry.uid} ({a.scope_path or 'anywhere'})",
)
queue(
    key="kyc",
    title="Payout details to approve",
    cap="record_payment",
    actions=(("approve", "Approve"), ("reject", "Reject")),
    items=lambda: PayoutProfile.objects.filter(state="submitted").select_related("user")[:100],
    describe=lambda k: f"{k.user.username}: {k.country_code}, {k.method} (account details are shown only to the bank step)",
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
        ("agents", "AI agents", "moderate"),
        ("jobs", "Scheduled jobs", "view_audit"),
        ("orders", "Orders", "record_payment"),
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
            "company": CompanySection,
            "suppliers": SupplierVerification,
            "campaigns": Campaign,
            "templates": MessageTemplate,
            "ads": Ad,
            "kyc": PayoutProfile,
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
        elif key == "company":
            es.moderate_company_section(obj, actor=actor, approve=action == "approve")
        elif key == "suppliers":
            campaigns.decide_supplier(obj, actor=actor, approve=action == "approve", note=note)
        elif key == "campaigns":
            campaigns.approve_campaign(obj, actor=actor)
        elif key == "kyc":
            ledger_services.decide_kyc(obj, actor=actor, approve=action == "approve", note=note)
        elif key == "ads":
            pl.decide_ad(obj, actor=actor, approve=action == "approve")
        elif key == "templates":
            obj.provider_state, obj.approved_by_id = "approved", actor.pk
            obj.save(update_fields=["provider_state", "approved_by_id"])
            audit("template.approve", actor=actor, object_type="template", object_uid=str(obj.pk))
        elif key == "takedowns":
            (
                mod.execute_erasure(obj, actor=actor)
                if action == "erase"
                else mod.refuse_takedown(obj, actor=actor, reason=note or "refused")
            )
    except (
        es.EntryError,
        mod.ModerationError,
        ps.PlaceError,
        campaigns.CampaignError,
        pl.PlacementError,
        ledger_services.LedgerError,
    ) as exc:
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


def _na(v):
    return "n/a" if v is None else v


def agents_page(request):
    from agents import services as ag
    from agents.models import AgentJob
    from volunteers import services as vs

    denied = _gate(request, "moderate")
    if denied:
        return denied
    rows = [
        [j.pk, j.kind, j.source.name, j.status, f"{j.spent_minor}/{j.budget_cap_minor}", j.stop_reason]
        for j in AgentJob.objects.select_related("source").order_by("-id")[:50]
    ]
    st, per = ag.cap_status(), ag.cost_per_verified()
    note = (
        f"Today {st['day']}/{st['day_cap']} ({st['day_pct']}%), "
        f"month {st['month']}/{st['month_cap']} ({st['month_pct']}%). "
        f"Cost per verified record: {_na(per['per_verified_minor'])} minor units. "
        f"Kill switch: {'ON' if ag.kill_switch_on() else 'off'}. Accuracy by source: "
        + (", ".join(f"{k} {v[2]:.0%} of {v[0]}" for k, v in vs.accuracy_by_source().items()) or "no audits yet")
    )
    return render(
        request,
        "catalog/staff/table.html",
        {
            "title": "AI agents",
            "head": ["Job", "Kind", "Source", "Status", "Spent", "Stopped because"],
            "rows": rows,
            "note": note,
            "robots": "noindex,nofollow",
        },
    )


def jobs_page(request):
    from core.models import JobRun

    denied = _gate(request, "view_audit")
    return denied or render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Scheduled jobs",
            "head": ["Job", "Last run", "Result", "Error"],
            "rows": [
                [j.name, j.last_run.strftime("%Y-%m-%d %H:%M") if j.last_run else "never", j.last_result, j.last_error]
                for j in JobRun.objects.order_by("name")
            ],
            "robots": "noindex,nofollow",
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


def statistics(request):
    """Aggregate statistics for institutions (rule R30): counts only, small cells hidden, no business named."""
    from analytics import extracts as ex

    denied = _gate(request, "run_extract")
    if denied:
        return denied
    scope = request.GET.get("scope", "").strip()
    slug = request.GET.get("type", "").strip()
    from taxonomy.models import Concept

    concept = Concept.objects.filter(kind="list_type", slug=slug).first() if slug else None
    report = ex.statistics_report(scope, concept)
    if request.GET.get("format") == "csv":
        from django.http import HttpResponse

        audit("statistics.export", actor=request.user, object_type="statistics", object_uid=scope or "world")
        resp = HttpResponse(ex.statistics_csv(report), content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = 'attachment; filename="statistics.csv"'
        return resp
    rows = [[k, v] for k, v in report.items() if not isinstance(v, dict)]
    rows += [[f"check: {k}", v] for k, v in report["by_level"].items()]
    rows += [[f"place: {k}", v] for k, v in report["by_child_place"].items()]
    return render(
        request,
        "catalog/staff/table.html",
        {"title": "Statistics report", "head": ["Measure", "Value"], "rows": rows, "robots": "noindex,nofollow"},
    )


def extracts(request):
    from analytics import extracts as ex
    from analytics.models import Extract
    from billing.models import Order
    from taxonomy.models import Concept

    denied = _gate(request, "run_extract")
    if denied:
        return denied
    if request.method == "POST":
        order = Order.objects.filter(ref=request.POST.get("order", "")).first() if request.POST.get("order") else None
        concept = Concept.objects.filter(kind="list_type", slug=request.POST.get("type", "")).first()
        try:
            made = ex.build_extract(
                request.user,
                request.POST.get("scope", "").strip(),
                concept,
                order=order,
                purpose=request.POST.get("purpose", ""),
                buyer_label=request.POST.get("buyer", ""),
            )
            messages.success(request, f"Extract {made.pk}: {made.row_count} rows, {made.trace_count} trace entries.")
        except ex.ExtractError as exc:
            messages.error(request, str(exc))
        return redirect("/staff/extracts/")
    rows = [
        [
            e.pk,
            e.scope_path or "world",
            e.order_ref or e.purpose,
            e.row_count,
            e.trace_count,
            f"/staff/extracts/{e.pk}/download/",
        ]
        for e in Extract.objects.order_by("-id")[:50]
    ]
    return render(
        request,
        "catalog/staff/table.html",
        {
            "title": "Extracts",
            "head": ["Extract", "Scope", "Order or purpose", "Rows", "Traces", "Download"],
            "rows": rows,
            "robots": "noindex,nofollow",
            "form": [
                ("scope", "Place path"),
                ("type", "List type slug"),
                ("order", "Paid order ref"),
                ("purpose", "Or purpose"),
                ("buyer", "Buyer label"),
            ],
        },
    )


def extract_download(request, pk):
    from analytics import extracts as ex
    from analytics.models import Extract

    denied = _gate(request, "run_extract")
    if denied:
        return denied
    obj = Extract.objects.filter(pk=pk).first()
    if obj is None:
        raise Http404
    from django.http import HttpResponse

    resp = HttpResponse(ex.read_extract(obj, request.user), content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{obj.file_name}"'
    resp["Cache-Control"] = "private, no-store"
    return resp


def ledger_page(request):
    """Reconciliation and payout batches (plan 12.5). Creating and approving a batch are different people."""
    from billing.reconcile import reconcile

    denied = _gate(request, "record_payment")
    if denied:
        return denied
    if request.method == "POST":
        action, batch = (
            request.POST.get("action"),
            PayoutBatch.objects.filter(pk=request.POST.get("batch") or 0).first(),
        )
        try:
            if action == "create":
                if not has_cap(request.user, "create_payout"):
                    return HttpResponseForbidden("Not allowed")
                ledger_services.create_batch(request.user)
            elif action == "approve" and batch:
                if not has_cap(request.user, "approve_payout"):
                    return HttpResponseForbidden("Not allowed")
                ledger_services.approve_batch(batch, approver=request.user)
            elif action == "paid" and batch:
                refs = {}
                for line in request.POST.get("refs", "").splitlines():
                    pid, _, ref = line.partition("=")
                    if pid.strip().isdigit() and ref.strip():
                        refs[int(pid)] = ref.strip()
                ledger_services.mark_batch_paid(batch, refs)
        except ledger_services.LedgerError as exc:
            messages.error(request, str(exc))
        return redirect("/staff/ledger/")
    batches = list(PayoutBatch.objects.order_by("-id")[:10])
    return render(
        request,
        "catalog/staff/ledger.html",
        {
            "results": reconcile(),
            "batches": [(b, list(b.payouts.select_related("user"))) for b in batches],
            "robots": "noindex,nofollow",
            "title": "Ledger",
        },
    )
