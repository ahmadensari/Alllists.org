"""Task queue for verification and review work, contributor levels and rewards (plan 14)."""

from django.conf import settings
from django.db import models

from core import clock


class Task(models.Model):
    class Kind(models.TextChoices):
        VERIFY = "verify"
        SURVEY = "survey"
        DEDUPE_REVIEW = "dedupe_review"
        AREA_REVIEW = "area_review"
        TRANSLATE = "translate"

    class State(models.TextChoices):
        OPEN = "open"
        ASSIGNED = "assigned"
        DONE = "done"
        SKIPPED = "skipped"

    kind = models.CharField(max_length=14, choices=Kind.choices)
    entry = models.ForeignKey("entries.Entry", null=True, blank=True, on_delete=models.CASCADE, related_name="tasks")
    place = models.ForeignKey("places.Place", null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="tasks"
    )
    state = models.CharField(max_length=10, choices=State.choices, default=State.OPEN)
    field_group = models.CharField(max_length=20, default="identity")
    due_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(default=dict, blank=True)
    minutes = models.PositiveSmallIntegerField(null=True, blank=True)  # logged to measure cost per record
    canary = models.BooleanField(default=False)  # a known answer used to test the surveyor
    created_at = models.DateTimeField(default=clock.now)
    done_at = models.DateTimeField(null=True, blank=True)


class ContributorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributor")
    level = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    ref_code = models.CharField(max_length=12, unique=True)
    accuracy = models.FloatField(null=True, blank=True)
    suspended = models.BooleanField(default=False)
    onboarded_at = models.DateTimeField(null=True, blank=True)
    declared_rights_at = models.DateTimeField(null=True, blank=True)


class Reward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rewards")
    kind = models.CharField(max_length=20)  # certificate, visible_credit, access_credit
    detail = models.CharField(max_length=120, blank=True)
    granted_at = models.DateTimeField(default=clock.now)
