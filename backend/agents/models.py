"""AI agent jobs and draft staging (plan 7.6, rule R35). Agents write only here; promotion is a separate service."""

from django.db import models

from core import clock


class AgentJob(models.Model):
    class Kind(models.TextChoices):
        DRAFT = "draft"
        SECOND_CHECK = "second_check"
        RECHECK = "recheck"

    class Status(models.TextChoices):
        QUEUED = "queued"
        RUNNING = "running"
        DONE = "done"
        FAILED = "failed"
        STOPPED = "stopped"  # a source refused, the budget ran out or the kill switch was on

    kind = models.CharField(max_length=14, choices=Kind.choices)
    source = models.ForeignKey("intake.Source", on_delete=models.PROTECT, related_name="agent_jobs")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.QUEUED)
    budget_cap_minor = models.PositiveIntegerField()
    spent_minor = models.PositiveIntegerField(default=0)
    tokens_in = models.PositiveIntegerField(default=0)
    tokens_out = models.PositiveIntegerField(default=0)
    model = models.CharField(max_length=60, blank=True)
    stop_reason = models.CharField(max_length=120, blank=True)
    started_at = models.DateTimeField(default=clock.now)
    finished_at = models.DateTimeField(null=True, blank=True)


class DraftEntry(models.Model):
    class State(models.TextChoices):
        STAGED = "staged"
        PROMOTED = "promoted"
        REJECTED = "rejected"

    job = models.ForeignKey(AgentJob, on_delete=models.CASCADE, related_name="drafts")
    raw = models.JSONField(default=dict)
    evidence_quotes = models.JSONField(default=dict)
    source_urls = models.JSONField(default=list)
    confidence = models.FloatField(default=0.0)
    cost_minor = models.PositiveIntegerField(default=0)
    state = models.CharField(max_length=10, choices=State.choices, default=State.STAGED)
    reason = models.CharField(max_length=160, blank=True)
    entry = models.ForeignKey("entries.Entry", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    created_at = models.DateTimeField(default=clock.now)
