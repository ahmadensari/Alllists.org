"""Append-only double-entry ledger, rate phases, sales, allocations and payouts (plan 12). Money is integer minor units."""

from django.conf import settings
from django.db import models

from core import clock
from core.crypto import EncryptedTextField


class RatePhase(models.Model):
    """A period with a contributor rate (50, 40, 30). The phase is locked on each entry when it is first accepted (R11)."""

    name = models.CharField(max_length=40)
    starts_on = models.DateField()
    ends_on = models.DateField(null=True, blank=True)
    rate_percent = models.PositiveSmallIntegerField()
    cap_months = models.PositiveSmallIntegerField(default=36)

    class Meta:
        ordering = ["starts_on"]


class LedgerAccount(models.Model):
    class Kind(models.TextChoices):
        CLEARING = "clearing"  # money received from buyers, not yet split
        PLATFORM = "platform"  # the platform's revenue
        FEES = "fees"  # provider fees owed
        TAX = "tax"  # tax collected
        HOLDING = "holding"  # contributor share inside the refund hold
        PAYABLE = "payable"  # contributor share released and owed
        PAYOUT = "payout"  # cash paid out
        REFUND = "refund"  # refunds paid back
        CREDIT = "credit"  # non-cash access credit (never money)

    kind = models.CharField(max_length=10, choices=Kind.choices)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    currency = models.CharField(max_length=3, default="USD")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kind", "user", "currency"], name="uniq_ledger_account")]


class LedgerTxn(models.Model):
    idempotency_key = models.CharField(max_length=80, unique=True)
    kind = models.CharField(max_length=12)  # sale, refund, release, payout, adjustment
    ref = models.CharField(max_length=60, blank=True)
    memo = models.CharField(max_length=200, blank=True)
    ts = models.DateTimeField(default=clock.now)
    reverses = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="reversed_by")


class LedgerPosting(models.Model):
    txn = models.ForeignKey(LedgerTxn, on_delete=models.PROTECT, related_name="postings")
    account = models.ForeignKey(LedgerAccount, on_delete=models.PROTECT, related_name="postings")
    amount_minor = models.BigIntegerField()  # signed; the postings of a transaction sum to zero per currency
    currency = models.CharField(max_length=3, default="USD")


class Sale(models.Model):
    class Kind(models.TextChoices):
        LIST = "list"
        SUBSCRIPTION = "subscription"
        LISTING = "listing"
        RANK = "rank"
        EXTRACT = "extract"
        OUTREACH = "outreach"
        AD = "ad"

    class State(models.TextChoices):
        RECORDED = "recorded"
        REFUNDED = "refunded"

    order_ref = models.CharField(max_length=40, unique=True)
    kind = models.CharField(max_length=14, choices=Kind.choices)
    scope_path = models.CharField(max_length=500, blank=True)
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    currency = models.CharField(max_length=3, default="USD")
    gross_minor = models.BigIntegerField()
    fees_minor = models.BigIntegerField(default=0)
    tax_minor = models.BigIntegerField(default=0)
    net_minor = models.BigIntegerField()
    state = models.CharField(max_length=10, choices=State.choices, default=State.RECORDED)
    txn = models.OneToOneField(LedgerTxn, on_delete=models.PROTECT, related_name="sale")
    ts = models.DateTimeField(default=clock.now)


class SaleAllocation(models.Model):
    """One line per contributor per sale (not per entry)."""

    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name="allocations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    entry_count = models.PositiveIntegerField()
    amount_minor = models.BigIntegerField()
    hold_until = models.DateTimeField()
    released_at = models.DateTimeField(null=True, blank=True)
    reversed_at = models.DateTimeField(null=True, blank=True)


class PayoutProfile(models.Model):
    """Who gets paid and how (plan 12.5, F14). Identity checks happen before the first payout; details are encrypted."""

    class KYC(models.TextChoices):
        SUBMITTED = "submitted"
        APPROVED = "approved"
        REJECTED = "rejected"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payout_profile")
    legal_name_enc = EncryptedTextField()
    country_code = models.CharField(max_length=2)
    method = models.CharField(max_length=30)  # bank, wallet, other
    account_enc = EncryptedTextField()
    tax_id_enc = EncryptedTextField(blank=True, default="")
    state = models.CharField(max_length=10, choices=KYC.choices, default=KYC.SUBMITTED)
    note = models.CharField(max_length=200, blank=True)
    decided_by_id = models.BigIntegerField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=clock.now)


class PayoutBatch(models.Model):
    """One payout cycle. Two people are needed: one creates, a different one approves (rule: separation of duties)."""

    class State(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        PAID = "paid"
        CANCELLED = "cancelled"

    currency = models.CharField(max_length=3, default="USD")
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    total_minor = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=clock.now)


class Payout(models.Model):
    class State(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        PAID = "paid"
        CANCELLED = "cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payouts")
    currency = models.CharField(max_length=3, default="USD")
    amount_minor = models.BigIntegerField()
    method = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    external_ref = models.CharField(max_length=80, blank=True)
    txn = models.ForeignKey(LedgerTxn, null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    batch = models.ForeignKey(PayoutBatch, null=True, blank=True, on_delete=models.PROTECT, related_name="payouts")
    created_at = models.DateTimeField(default=clock.now)
