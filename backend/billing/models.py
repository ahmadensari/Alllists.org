"""Products, orders, payments and invoices (plan 12.4)."""

from django.conf import settings
from django.db import models

from core import clock


class Product(models.Model):
    class Kind(models.TextChoices):
        SUBSCRIPTION = "subscription"  # scoped read access for a period
        LIST_ACCESS = "list_access"  # time-limited full access to one list
        LISTING = "listing"  # company page for one entry
        RANK = "rank"
        EXTRACT = "extract"
        OUTREACH = "outreach"
        AD = "ad"

    key = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=14, choices=Kind.choices)
    price_minor = models.BigIntegerField()
    currency = models.CharField(max_length=3, default="USD")
    period_days = models.PositiveIntegerField(default=30)
    active = models.BooleanField(default=True)


class Order(models.Model):
    class State(models.TextChoices):
        PENDING = "pending"
        PAID = "paid"
        FULFILLED = "fulfilled"
        REFUNDED = "refunded"
        CANCELLED = "cancelled"

    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="+")
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    currency = models.CharField(max_length=3)
    amount_minor = models.BigIntegerField()
    tax_minor = models.BigIntegerField(default=0)
    scope_path = models.CharField(max_length=500, blank=True)
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    entry = models.ForeignKey("entries.Entry", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    campaign_id = models.PositiveIntegerField(null=True, blank=True)
    ad_id = models.PositiveIntegerField(null=True, blank=True)
    tax_rate = models.CharField(max_length=10, default="0")  # percent at the time of the order
    billing = models.JSONField(default=dict, blank=True)  # name, address, tax number given by the buyer
    created_at = models.DateTimeField(default=clock.now)
    ref = models.CharField(max_length=40, unique=True)


class Payment(models.Model):
    class State(models.TextChoices):
        SUCCEEDED = "succeeded"
        FAILED = "failed"
        REFUNDED = "refunded"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    provider = models.CharField(max_length=20)  # manual, or a gateway adapter name
    provider_ref = models.CharField(max_length=80)
    amount_minor = models.BigIntegerField()
    fees_minor = models.BigIntegerField(default=0)
    state = models.CharField(max_length=10, choices=State.choices)
    recorded_by_id = models.BigIntegerField(null=True, blank=True)
    raw = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["provider", "provider_ref"], name="uniq_payment_ref")]


class InvoiceCounter(models.Model):
    """Gap-free numbering: one counter row per year, locked while a number is taken."""

    year = models.PositiveSmallIntegerField(unique=True)
    last = models.PositiveIntegerField(default=0)


class Invoice(models.Model):
    class Kind(models.TextChoices):
        INVOICE = "invoice"
        CREDIT_NOTE = "credit_note"

    number = models.CharField(max_length=20, unique=True)
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.INVOICE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="invoices")
    credit_for = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="credits")
    issued_at = models.DateTimeField(default=clock.now)
    currency = models.CharField(max_length=3, default="USD")
    seller = models.JSONField(default=dict, blank=True)  # legal name, address, tax number at the time of issue
    buyer = models.JSONField(default=dict, blank=True)
    tax_rate = models.CharField(max_length=10, default="0")
    lines = models.JSONField(default=list)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order"], condition=models.Q(kind="invoice"), name="one_invoice_per_order")
        ]
