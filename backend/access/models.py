"""Plans, subscriptions and entitlements (plan 4.2.6, 9.5). Subscriber is an entitlement with a scope, not a role."""

from django.conf import settings
from django.db import models

from core import clock


class Plan(models.Model):
    key = models.SlugField(unique=True)  # free, subscriber_scope, listing_basic, listing_company, rank_city, extract
    name = models.CharField(max_length=80)
    price_minor = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=3, default="USD")
    interval_days = models.PositiveIntegerField(default=30)
    features = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)


class Subscription(models.Model):
    class State(models.TextChoices):
        ACTIVE = "active"
        CANCELLED = "cancelled"
        EXPIRED = "expired"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="+")
    scope_path = models.CharField(max_length=500, blank=True)  # place subtree; "" means the whole world
    scope_concept = models.ForeignKey(
        "taxonomy.Concept", null=True, blank=True, on_delete=models.PROTECT, related_name="+"
    )
    state = models.CharField(max_length=10, choices=State.choices, default=State.ACTIVE)
    period_start = models.DateTimeField(default=clock.now)
    period_end = models.DateTimeField()
    provider_ref = models.CharField(max_length=80, blank=True)


class Entitlement(models.Model):
    class Kind(models.TextChoices):
        SUBSCRIPTION = "subscription"
        LIST_ACCESS = "list_access"
        EXTRACT = "extract"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="entitlements")
    kind = models.CharField(max_length=14, choices=Kind.choices)
    scope_path = models.CharField(max_length=500, blank=True)
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    valid_from = models.DateTimeField(default=clock.now)
    valid_to = models.DateTimeField()
    source = models.CharField(max_length=40, blank=True)  # order or subscription reference
    revoked_at = models.DateTimeField(null=True, blank=True)


class QuotaCounter(models.Model):
    subject = models.CharField(max_length=64)  # keyed hash of user id or address
    key = models.CharField(max_length=30)
    day = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["subject", "key", "day"], name="uniq_quota_counter")]
