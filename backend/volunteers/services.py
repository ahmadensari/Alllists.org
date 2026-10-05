"""Task queue, surveyor workflow, levels and ref codes (plan 14). Surveyors never get tasks on entries they added."""

import secrets
from datetime import timedelta

from django.db import transaction
from django.db.models import Q

from core import clock
from core.models import audit
from entries import services as es
from entries.models import Entry

from .models import ContributorProfile, Reward, Task

LEVEL_STEPS = [0, 5, 25, 100, 500]  # verified contributions needed for levels 1..4


def ensure_profile(user):
    prof, _ = ContributorProfile.objects.get_or_create(user=user, defaults={"ref_code": secrets.token_hex(4)})
    return prof


def queue_verification(entry, *, field_group="identity", canary=False, due_days=14):
    return Task.objects.create(
        kind=Task.Kind.VERIFY,
        entry=entry,
        field_group=field_group,
        canary=canary,
        due_at=clock.now() + timedelta(days=due_days),
    )


def queue_unchecked(limit=100):
    """One verify task for each draft entry that has no open task yet."""
    made = 0
    for e in Entry.objects.filter(publish_state="draft", deleted_at__isnull=True, merged_into__isnull=True).exclude(
        tasks__state__in=["open", "assigned"]
    )[:limit]:
        queue_verification(e)
        made += 1
    return made


@transaction.atomic
def take_next_task(user):
    """Assign the oldest open task the user may do. A surveyor is never given an entry they added (rule R07)."""
    prof = ensure_profile(user)
    if prof.suspended:
        return None
    task = (
        Task.objects.select_for_update(skip_locked=True, of=("self",))
        .filter(state=Task.State.OPEN, kind=Task.Kind.VERIFY)
        .exclude(entry__created_by=user)
        .exclude(audit_sample__original_verifier_id=user.pk)
        .order_by("created_at")
        .first()
    )
    if task is None:
        return None
    task.state, task.assigned_to = Task.State.ASSIGNED, user
    task.save(update_fields=["state", "assigned_to"])
    return task


@transaction.atomic
def complete_task(task, *, user, outcome, evidence="", method="call", minutes=None):
    """outcome: confirmed, closed, wrong, unreachable. A confirmed outcome records a surveyor check."""
    if task.assigned_to_id != user.pk or task.state != Task.State.ASSIGNED:
        raise es.GuardError("this task is not assigned to you")
    if outcome not in ("confirmed", "closed", "wrong", "unreachable"):
        raise es.GuardError("unknown outcome")
    if outcome in ("confirmed", "closed") and not evidence.strip():
        raise es.GuardError("evidence text is required")
    if task.field_group == "audit":
        # an audit re-checks an already published entry: it measures accuracy and records no new check
        from .models import AuditSample

        sample = AuditSample.objects.get(task=task)
        sample.correct = outcome == "confirmed"
        sample.save(update_fields=["correct"])
        if outcome == "closed":
            es.update_entry(task.entry, actor=user, status=Entry.Status.PERM_CLOSED)
    elif outcome == "confirmed":
        es.record_verification(
            task.entry, field_group=task.field_group, level="surveyor", actor=user, method=method, evidence=evidence
        )
    elif outcome == "closed":
        es.update_entry(task.entry, actor=user, status=Entry.Status.PERM_CLOSED)
    task.state, task.done_at, task.minutes = Task.State.DONE, clock.now(), minutes
    task.result = {"outcome": outcome, "method": method}
    task.save()
    prof = ensure_profile(user)
    prof.points += 1
    prof.level = max(i for i, n in enumerate(LEVEL_STEPS) if prof.points >= n or i == 0)
    if task.canary:
        _score_canary(prof, task, outcome)
    prof.save()
    audit("task.complete", actor=user, object_type="task", object_uid=str(task.pk), payload={"outcome": outcome})
    return task


def _score_canary(prof, task, outcome):
    """A canary is a fake shop only we know: the right answer is "unreachable" or "wrong". Accuracy under 0.8 suspends."""
    correct = outcome in ("unreachable", "wrong")
    done = Task.objects.filter(assigned_to=prof.user, canary=True, state=Task.State.DONE).count()
    prev = prof.accuracy if prof.accuracy is not None else 1.0
    prof.accuracy = (prev * max(done - 1, 0) + (1.0 if correct else 0.0)) / max(done, 1)
    if done >= 3 and prof.accuracy < 0.8:
        prof.suspended = True
        audit("surveyor.suspend", object_type="user", object_uid=str(prof.user_id), payload={"accuracy": prof.accuracy})


def grant_reward(user, kind, detail=""):
    return Reward.objects.create(user=user, kind=kind, detail=detail)


def completion_rate(days=14):
    since = clock.now() - timedelta(days=days)
    assigned = Task.objects.filter(Q(created_at__gte=since), state__in=["assigned", "done", "skipped"]).count()
    done = Task.objects.filter(created_at__gte=since, state="done").count()
    return (done / assigned) if assigned else None


# ---- canaries and audit samples (plan 6.4, T1.03) -----------------------------------------------------------------

AUDIT_SAMPLE_SIZE = 385  # about 95 percent confidence, 5 percent margin, for a large population


def plant_canaries(place, concept, n, *, purpose="verifier"):
    """Create fake draft entries. Surveyors are tasked with them; the right answer is that nobody can be reached."""
    from .models import CanaryEntry

    made = []
    for i in range(n):
        e = es.create_entry(
            name=f"Canary {secrets.token_hex(3)} Traders",
            place=place,
            primary_concept=concept,
            created_via=Entry.CreatedVia.AGENT,
            source=__import__("intake.models", fromlist=["Source"]).Source.objects.get_or_create(
                name="Platform canaries", defaults=dict(tier="green", allowed_uses=["agent_fetch", "display", "import"])
            )[0],
            contacts=[("phone", f"+0000{secrets.randbelow(10**7):07d}")],
        )
        CanaryEntry.objects.create(entry=e, purpose=purpose)
        if purpose == "verifier":
            queue_verification(e, canary=True)
        made.append(e)
    return made


def queue_audit_sample(n=AUDIT_SAMPLE_SIZE, *, seed=None):
    """Pick random published entries and queue an audit task for each, once. Returns how many were queued."""
    import random

    from .models import AuditSample

    rng = random.Random(seed)
    ids = list(
        Entry.objects.filter(publish_state="published", deleted_at__isnull=True, canary__isnull=True)
        .exclude(audit_samples__isnull=False)
        .values_list("pk", flat=True)
    )
    queued = 0
    for pk in rng.sample(ids, min(n, len(ids))):
        e = Entry.objects.get(pk=pk)
        t = Task.objects.create(kind=Task.Kind.VERIFY, entry=e, field_group="audit")
        last = e.verification_events.filter(state="verified", actor_id__isnull=False).order_by("-id").first()
        AuditSample.objects.create(
            entry=e, task=t, source=e.source, original_verifier_id=last.actor_id if last else None
        )
        queued += 1
    return queued


def accuracy_by_source():
    """{source name: (checked, correct, accuracy)} from completed audit samples."""
    from .models import AuditSample

    out = {}
    for s in AuditSample.objects.filter(correct__isnull=False).select_related("source"):
        name = s.source.name if s.source else "contributors"
        c, ok, _ = out.get(name, (0, 0, 0))
        out[name] = (c + 1, ok + int(s.correct), 0)
    return {k: (c, ok, ok / c) for k, (c, ok, _) in out.items()}


def accuracy_by_verifier():
    from .models import AuditSample

    out = {}
    for s in AuditSample.objects.filter(correct__isnull=False, original_verifier_id__isnull=False):
        c, ok = out.get(s.original_verifier_id, (0, 0))
        out[s.original_verifier_id] = (c + 1, ok + int(s.correct))
    return {k: (c, ok, ok / c) for k, (c, ok) in out.items()}
