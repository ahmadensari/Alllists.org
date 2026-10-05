"""Surveyor task screens (plan 14.2): large targets, one task at a time, evidence required, minutes logged."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from accounts.roles import has_cap
from core.models import audit
from entries import services as es
from volunteers import services as vs
from volunteers.models import Task

LOGIN = "/account/login/"


@login_required(login_url=LOGIN)
@require_http_methods(["GET", "POST"])
def my_tasks(request):
    if not has_cap(request.user, "verify"):
        return HttpResponseForbidden("Verification tasks are for surveyors.")
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
def contributor_page(request):
    prof = vs.ensure_profile(request.user)
    from entries.models import CreditEvent, Entry

    added = Entry.objects.filter(created_by=request.user).count()
    credit = CreditEvent.objects.filter(user=request.user, kind="added")
    return render(
        request,
        "catalog/tasks/contributor.html",
        {
            "prof": prof,
            "added": added,
            "eligible": credit.filter(eligible=True).count(),
            "waiting": credit.filter(eligible=False).count(),
            "ref_link": request.build_absolute_uri(f"/?ref={prof.ref_code}"),
            "robots": "noindex,nofollow",
            "title": "Contributor",
        },
    )
