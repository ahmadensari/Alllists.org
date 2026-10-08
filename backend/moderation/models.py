"""Reports, suggested edits and takedowns (plan 4.2.7, 15). Every entry has a free way to correct or remove data."""

from django.conf import settings
from django.db import models

from core import clock


class Report(models.Model):
    class Kind(models.TextChoices):
        CLOSED = "closed"
        WRONG = "wrong"
        DUPLICATE = "duplicate"
        FAKE = "fake"
        REMOVE_MY_DATA = "remove_my_data"
        SUGGEST_EDIT = "suggest_edit"
        CLAIM_DISPUTE = "claim_dispute"

    class State(models.TextChoices):
        OPEN = "open"
        ASSIGNED = "assigned"
        UPHELD = "upheld"
        REJECTED = "rejected"

    entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="reports")
    kind = models.CharField(max_length=20, choices=Kind.choices)
    text = models.TextField(blank=True, max_length=2000)
    reporter_hash = models.CharField(max_length=64, blank=True)  # keyed hash of the address; never the address itself
    reporter_contact_enc = models.TextField(blank=True)  # optional reply contact, encrypted
    state = models.CharField(max_length=10, choices=State.choices, default=State.OPEN)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    resolution = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=clock.now)
    decided_at = models.DateTimeField(null=True, blank=True)


class SuggestedEdit(models.Model):
    class State(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="suggested_edits")
    field_key = models.CharField(max_length=60)
    new_value = models.JSONField()
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="+")
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    created_at = models.DateTimeField(default=clock.now)
    decided_by_id = models.BigIntegerField(null=True, blank=True)


class Takedown(models.Model):
    """A removal or erasure request with its legal basis and deadline (plan 15.3)."""

    class State(models.TextChoices):
        OPEN = "open"
        DONE = "done"
        REFUSED = "refused"

    entry = models.ForeignKey("entries.Entry", null=True, on_delete=models.SET_NULL, related_name="takedowns")
    requester_hash = models.CharField(max_length=64, blank=True)
    kind = models.CharField(max_length=20)  # erasure, correction, legal
    legal_basis = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=10, choices=State.choices, default=State.OPEN)
    due_at = models.DateTimeField(null=True, blank=True)
    log = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=clock.now)
    done_at = models.DateTimeField(null=True, blank=True)
