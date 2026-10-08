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


# ---- campaigns (plan 13, phase P4) -------------------------------------------------------------------------------


class SupplierVerification(models.Model):
    """A buyer must be a verified supplier before sending campaigns (V8, G5)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supplier")
    company = models.CharField(max_length=120)
    state = models.CharField(max_length=10, default="pending")  # pending, verified, rejected, paused
    decided_by_id = models.BigIntegerField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)


class MessageTemplate(models.Model):
    key = models.SlugField()
    channel = models.CharField(max_length=10)
    language = models.CharField(max_length=5, default="en")
    body = models.TextField()  # placeholders in braces: {company}, {category}, {note}
    provider_state = models.CharField(max_length=10, default="draft")  # draft, submitted, approved
    approved_by_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["key", "channel", "language"], name="uniq_message_template")]


class Campaign(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft"
        PENDING = "pending"
        APPROVED = "approved"
        SENDING = "sending"
        DONE = "done"
        PAUSED = "paused"

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="campaigns")
    scope_path = models.CharField(max_length=500)
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.PROTECT, related_name="+")
    template = models.ForeignKey(MessageTemplate, on_delete=models.PROTECT, related_name="+")
    variables = models.JSONField(default=dict, blank=True)
    channel = models.CharField(max_length=10)
    country_code = models.CharField(max_length=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    budget_minor = models.PositiveIntegerField(default=0)
    spent_minor = models.PositiveIntegerField(default=0)
    funded = models.BooleanField(default=False)
    approved_by_id = models.BigIntegerField(null=True, blank=True)
    pause_reason = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(default=clock.now)


class Message(models.Model):
    class State(models.TextChoices):
        QUEUED = "queued"
        SENT = "sent"
        DELIVERED = "delivered"
        READ = "read"
        REPLIED = "replied"
        FAILED = "failed"
        OPTED_OUT = "opted_out"

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="messages")
    entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="+")
    contact = models.ForeignKey("entries.Contact", on_delete=models.CASCADE, related_name="+")
    channel = models.CharField(max_length=10)
    state = models.CharField(max_length=10, choices=State.choices, default=State.QUEUED)
    provider_id = models.CharField(max_length=80, blank=True, db_index=True)
    reply_text = models.TextField(blank=True)
    cost_minor = models.PositiveIntegerField(default=0)
    ts = models.DateTimeField(default=clock.now)


class DeliveryEvent(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="events")
    event = models.CharField(max_length=12)
    payload = models.JSONField(default=dict, blank=True)
    ts = models.DateTimeField(default=clock.now)
