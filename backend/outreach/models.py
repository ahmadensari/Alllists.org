"""Opt-in, suppression, enquiry relay and outbox (plan 13). Contacts are used here and never shown (rule R02)."""

from django.conf import settings
from django.db import models

from core import clock


class Optin(models.Model):
    """Append-only record of agreement to be messaged. `withdrawn_at` is the only field that changes."""

    contact = models.ForeignKey("entries.Contact", on_delete=models.CASCADE, related_name="optins")
    channel = models.CharField(max_length=10)  # email, whatsapp, sms
    topics = models.JSONField(default=list, blank=True)
    method = models.CharField(max_length=40)  # claim_otp, form
    wording_version = models.CharField(max_length=20)
    evidence_text = models.CharField(max_length=200, blank=True)
    ts = models.DateTimeField(default=clock.now)
    withdrawn_at = models.DateTimeField(null=True, blank=True)


class Suppression(models.Model):
    """Global do-not-contact list by keyed hash. Survives re-imports (rule R29)."""

    value_hash = models.CharField(max_length=64, db_index=True)
    channel = models.CharField(max_length=10, blank=True)  # blank means every channel
    ts = models.DateTimeField(default=clock.now)
    reason = models.CharField(max_length=40, blank=True)


class OutboxMessage(models.Model):
    """Messages waiting for a provider adapter (SMS, WhatsApp, OTP). Email goes out directly."""

    channel = models.CharField(max_length=10)
    kind = models.CharField(max_length=12)  # otp, enquiry, campaign
    contact = models.ForeignKey("entries.Contact", on_delete=models.CASCADE, related_name="+")
    body = models.TextField()
    state = models.CharField(max_length=10, default="queued")  # queued, sent, failed
    created_at = models.DateTimeField(default=clock.now)
    sent_at = models.DateTimeField(null=True, blank=True)


class ClaimOtp(models.Model):
    entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="+")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    contact = models.ForeignKey("entries.Contact", on_delete=models.CASCADE, related_name="+")
    code_hash = models.CharField(max_length=64)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    used_at = models.DateTimeField(null=True, blank=True)


class Enquiry(models.Model):
    """One message to one or many businesses, relayed without revealing contacts."""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enquiries")
    text = models.TextField(max_length=2000)
    reply_to_enc = models.TextField()
    scope_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=clock.now)


class EnquiryRecipient(models.Model):
    class State(models.TextChoices):
        DELIVERED = "delivered"
        QUEUED = "queued"
        NOT_REACHABLE = "not_reachable"
        SUPPRESSED = "suppressed"

    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name="recipients")
    entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="+")
    state = models.CharField(max_length=14, choices=State.choices)
    replied_at = models.DateTimeField(null=True, blank=True)
