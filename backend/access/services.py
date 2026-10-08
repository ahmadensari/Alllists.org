from datetime import timedelta

from django.db import transaction

from core import clock
from core.models import audit

from .models import Entitlement, Plan, Subscription


@transaction.atomic
def grant_subscription(user, plan, *, scope_path="", concept=None, days=None, source="manual", actor=None, now=None):
    """Grant a scoped subscription and its entitlement (manual grant first, plan P3.04)."""
    now = now or clock.now()
    days = days or plan.interval_days
    end = now + timedelta(days=days)
    sub = Subscription.objects.create(
        user=user,
        plan=plan,
        scope_path=scope_path,
        scope_concept=concept,
        period_start=now,
        period_end=end,
        provider_ref=source,
    )
    ent = Entitlement.objects.create(
        user=user,
        kind=Entitlement.Kind.SUBSCRIPTION,
        scope_path=scope_path,
        concept=concept,
        valid_from=now,
        valid_to=end,
        source=f"subscription:{sub.pk}",
    )
    audit(
        "subscription.grant",
        actor=actor,
        object_type="user",
        object_uid=str(user.pk),
        payload={"plan": plan.key, "scope": scope_path, "days": days},
    )
    return sub, ent


def revoke_entitlements(user, *, actor=None, now=None):
    now = now or clock.now()
    n = Entitlement.objects.filter(user=user, revoked_at__isnull=True).update(revoked_at=now)
    Subscription.objects.filter(user=user, state="active").update(state="cancelled")
    audit("subscription.revoke", actor=actor, object_type="user", object_uid=str(user.pk), payload={"count": n})
    return n


def active_scopes(user, now=None):
    """[(scope_path, concept_id or None)] of live subscription-like entitlements."""
    if not getattr(user, "is_authenticated", False):
        return []
    now = now or clock.now()
    qs = Entitlement.objects.filter(
        user=user,
        revoked_at__isnull=True,
        valid_from__lte=now,
        valid_to__gt=now,
        kind__in=[Entitlement.Kind.SUBSCRIPTION, Entitlement.Kind.LIST_ACCESS],
    )
    return [(e.scope_path, e.concept_id) for e in qs]


def seed_plans():
    Plan.objects.get_or_create(key="free", defaults=dict(name="Free"))
    Plan.objects.get_or_create(
        key="subscriber_scope", defaults=dict(name="Subscriber (scope)", price_minor=0, interval_days=30)
    )
    Plan.objects.get_or_create(key="listing_company", defaults=dict(name="Company page", interval_days=90))
