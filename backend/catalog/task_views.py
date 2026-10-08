"""Surveyor task screens (plan 14.2): large targets, one task at a time, evidence required, minutes logged."""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.roles import has_cap
from core import clock
from core.models import audit
from entries import services as es
from volunteers import onboarding, rewards
from volunteers import services as vs
from volunteers.models import Task

LOGIN = "/account/login/"


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def my_tasks(request):
    if not has_cap(request.user, "verify"):
        return HttpResponseForbidden("Verification tasks are for surveyors.")
    if not onboarding.is_onboarded(request.user):
        return redirect("/account/contributor/onboarding/")
    if request.method == "POST" and request.POST.get("action") == "take":
        task = vs.take_next_task(request.user)
        if task is None:
            messages.info(request, "No tasks are waiting right now.")
        else:
            return redirect(f"/account/tasks/{task.pk}/")
    mine = Task.objects.filter(assigned_to=request.user, state="assigned").select_related("entry")
    return render(
        request, "catalog/tasks/list.html", {"tasks": mine, "robots": "noindex,nofollow", "title": "My tasks"}
    )


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def task_detail(request, pk):
    task = Task.objects.filter(pk=pk, assigned_to=request.user).select_related("entry", "entry__place").first()
    if task is None or not has_cap(request.user, "verify"):
        raise Http404
    errors, revealed = [], None
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "reveal" and task.state == "assigned":
            # The one place contact values are shown: the assigned surveyor, for this task only, and every reveal is audited.
            revealed = [(c.kind, c.value_enc) for c in task.entry.contact_set.all()]
            audit(
                "contact.reveal",
                actor=request.user,
                object_type="task",
                object_uid=str(task.pk),
                country_code=task.entry.country_code,
                payload={"entry": task.entry.uid, "count": len(revealed)},
            )
        elif action == "complete":
            try:
                minutes = int(request.POST.get("minutes") or 0) or None
            except ValueError:
                minutes = None
            try:
                vs.complete_task(
                    task,
                    user=request.user,
                    outcome=request.POST.get("outcome", ""),
                    evidence=request.POST.get("evidence", ""),
                    method=request.POST.get("method", "call"),
                    minutes=minutes,
                )
            except es.GuardError as exc:
                errors.append(("evidence", str(exc)))
            else:
                messages.success(request, "Recorded. Thank you.")
                return redirect("/account/tasks/")
    return render(
        request,
        "catalog/tasks/detail.html",
        {"task": task, "errors": errors, "revealed": revealed, "robots": "noindex,nofollow", "title": "Task"},
    )


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def contributor_page(request):
    from analytics.models import Event
    from accounts.models import Profile
    from entries.models import CreditEvent, Entry
    from volunteers.models import Reward

    prof = vs.ensure_profile(request.user)
    if request.method == "POST":
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if request.POST.get("action") == "credit":
            prof.show_credit = bool(request.POST.get("show_credit"))
            prof.save(update_fields=["show_credit"])
            name = request.POST.get("display_name", "").strip()[:60]
            if name:
                profile.display_name = name
                profile.save(update_fields=["display_name"])
            messages.success(request, "Saved.")
        return redirect("/account/contributor/")
    added = Entry.objects.filter(created_by=request.user).count()
    credit = CreditEvent.objects.filter(user=request.user, kind="added")
    visits = Event.objects.filter(name="ref_visit", props__ref=prof.ref_code)
    next_level = next((n for n in vs.LEVEL_STEPS if n > prof.points), None)
    return render(
        request,
        "catalog/tasks/contributor.html",
        {
            "prof": prof,
            "added": added,
            "eligible": credit.filter(eligible=True).count(),
            "waiting": credit.filter(eligible=False).count(),
            "ref_link": request.build_absolute_uri(f"/?ref={prof.ref_code}"),
            "visits_total": visits.count(),
            "visits_7d": visits.filter(ts__gte=clock.now() - timedelta(days=7)).count(),
            "certificates": Reward.objects.filter(user=request.user, kind="certificate").order_by("granted_at"),
            "credits": Reward.objects.filter(user=request.user, kind="access_credit"),
            "to_next": (next_level - prof.points) if next_level else None,
            "onboarded": prof.onboarded_at is not None,
            "display_name": getattr(getattr(request.user, "profile", None), "display_name", ""),
            "robots": "noindex,nofollow",
            "title": "Contributor",
        },
    )


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def onboarding_page(request):
    result = None
    if request.method == "POST":
        answers = {k: request.POST.get(f"q_{k}", "") for k, *_ in onboarding.QUESTIONS}
        result = onboarding.submit(request.user, answers, declared_rights=bool(request.POST.get("rights")))
        if result[1]:
            messages.success(request, "Welcome. You can now add entries and, with a surveyor role, take checks.")
            return redirect("/account/contributor/")
    return render(
        request,
        "catalog/tasks/onboarding.html",
        {
            "questions": onboarding.questions(getattr(request, "lang", "en")),
            "result": result,
            "pass_mark": onboarding.PASS_MARK,
            "total": len(onboarding.QUESTIONS),
            "robots": "noindex,nofollow",
            "title": "Contributor onboarding",
        },
    )


@login_required(login_url=LOGIN)
def certificate_page(request, pk):
    r = rewards.Reward.objects.filter(pk=pk, user=request.user, kind="certificate").first()
    if r is None:
        raise Http404
    return render(
        request,
        "catalog/tasks/certificate.html",
        {
            "reward": r,
            "verify_url": request.build_absolute_uri(f"/certificate/{r.code}/"),
            "robots": "noindex,nofollow",
            "title": "Certificate",
        },
    )


def certificate_verify(request, code):
    info = rewards.verify_certificate(code)
    if info is None:
        raise Http404
    return render(
        request,
        "catalog/tasks/certificate_verify.html",
        {"info": info, "robots": "noindex,nofollow", "title": "Certificate"},
    )
