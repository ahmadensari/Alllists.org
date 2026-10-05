"""Orders, payments and fulfilment (plan 12.4). Manual receipts first; gateway webhooks use the same recording path."""

import hmac
import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.db import IntegrityError, transaction

from access import services as access_services
from access.models import Entitlement, Plan
from core import clock
from core.models import audit
from entries import services as es
from ledger import services as ledger
from ledger.models import Sale

from .models import Invoice, Order, Payment, Product

KIND_TO_SALE = {
    "subscription": Sale.Kind.SUBSCRIPTION,
    "list_access": Sale.Kind.LIST,
    "listing": Sale.Kind.LISTING,
    "rank": Sale.Kind.RANK,
    "extract": Sale.Kind.EXTRACT,
}


class BillingError(ValueError):
    pass


def tax_for(country_code, amount_minor):
    """Tax in minor units from a per-country percentage in settings; none when unconfigured."""
    rate = Decimal(str(getattr(settings, "TAX_RATES", {}).get((country_code or "").upper(), "0")))
    return int((Decimal(amount_minor) * rate / Decimal(100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def new_ref():
    from core.ulid import new_ulid

    return "O" + new_ulid()[:12]


@transaction.atomic
def create_order(buyer, product, *, scope_path="", concept=None, entry=None):
    if not product.active:
        raise BillingError("this product is not on sale")
    if product.kind == Product.Kind.LISTING:
        if entry is None or not es.company_page_allowed(entry):
            raise BillingError("a company page needs an eligible entry")
        if not es.is_owner(entry, buyer):
            raise BillingError("only the owner can buy a company page")
    elif (
        product.kind in (Product.Kind.SUBSCRIPTION, Product.Kind.LIST_ACCESS)
        and concept is None
        and not scope_path
        and product.kind == Product.Kind.LIST_ACCESS
    ):
        raise BillingError("choose what to access")
    country = scope_path.split(".")[0] if scope_path else (entry.country_code if entry else "")
    tax = tax_for(country, product.price_minor)
    order = Order.objects.create(
        buyer=buyer,
        product=product,
        currency=product.currency,
        amount_minor=product.price_minor + tax,
        tax_minor=tax,
        scope_path=scope_path,
        concept=concept,
        entry=entry,
        ref=new_ref(),
    )
    audit("order.create", actor=buyer, object_type="order", object_uid=order.ref, payload={"product": product.key})
    return order


@transaction.atomic
def record_payment(order, *, provider, provider_ref, amount_minor, fees_minor=0, actor=None, raw=None, now=None):
    """Record a successful payment. Safe to repeat: the same provider reference never counts twice."""
    now = now or clock.now()
    existing = Payment.objects.filter(provider=provider, provider_ref=provider_ref).first()
    if existing:
        return existing, False
    if order.state not in (Order.State.PENDING,):
        raise BillingError(f"order is {order.state}")
    if amount_minor != order.amount_minor:
        raise BillingError("the amount paid does not match the order")
    try:
        pay = Payment.objects.create(
            order=order,
            provider=provider,
            provider_ref=provider_ref,
            amount_minor=amount_minor,
            fees_minor=fees_minor,
            state=Payment.State.SUCCEEDED,
            recorded_by_id=getattr(actor, "pk", None),
            raw=raw or {},
        )
    except IntegrityError:
        return Payment.objects.get(provider=provider, provider_ref=provider_ref), False
    order.state = Order.State.PAID
    order.save(update_fields=["state"])
    fulfil(order, pay, now=now)
    audit(
        "payment.record",
        actor=actor,
        object_type="order",
        object_uid=order.ref,
        payload={"provider": provider, "amount": amount_minor},
    )
    return pay, True


@transaction.atomic
def fulfil(order, payment, *, now=None):
    now = now or clock.now()
    p = order.product
    source = f"order:{order.ref}"
    if p.kind == Product.Kind.SUBSCRIPTION:
        plan = Plan.objects.get(key="subscriber_scope")
        access_services.grant_subscription(
            order.buyer,
            plan,
            scope_path=order.scope_path,
            concept=order.concept,
            days=p.period_days,
            source=source,
            now=now,
        )
    elif p.kind == Product.Kind.LIST_ACCESS:
        from datetime import timedelta

        Entitlement.objects.create(
            user=order.buyer,
            kind=Entitlement.Kind.LIST_ACCESS,
            scope_path=order.scope_path,
            concept=order.concept,
            valid_from=now,
            valid_to=now + timedelta(days=p.period_days),
            source=source,
        )
    elif p.kind == Product.Kind.LISTING:
        es.activate_company_plan(order.entry, days=p.period_days, actor=order.buyer)
    ledger.record_sale(
        order.ref,
        KIND_TO_SALE[p.kind],
        gross=order.amount_minor,
        fees=payment.fees_minor,
        tax=order.tax_minor,
        currency=order.currency,
        scope_path=order.scope_path,
        concept=order.concept,
        now=now,
    )
    order.state = Order.State.FULFILLED
    order.save(update_fields=["state"])
    Invoice.objects.get_or_create(
        order=order,
        defaults={
            "number": f"AL-{now.year}-{order.pk:06d}",
            "lines": [
                {"item": p.name, "amount_minor": order.amount_minor - order.tax_minor},
                {"item": "Tax", "amount_minor": order.tax_minor},
            ],
        },
    )


@transaction.atomic
def refund_order(order, *, actor):
    if order.state != Order.State.FULFILLED:
        raise BillingError("only a fulfilled order can be refunded")
    sale = Sale.objects.get(order_ref=order.ref)
    ledger.refund_sale(sale, actor=actor)
    Entitlement.objects.filter(source__in=[f"order:{order.ref}"]).update(revoked_at=clock.now())
    Entitlement.objects.filter(
        source__startswith="subscription:", user=order.buyer, valid_from__gte=order.created_at
    ).update(revoked_at=clock.now())
    order.state = Order.State.REFUNDED
    order.save(update_fields=["state"])
    order.payments.update(state=Payment.State.REFUNDED)
    audit("order.refund", actor=actor, object_type="order", object_uid=order.ref)
    return order


# ---- gateway webhook (adapter-neutral, signed) ------------------------------------------------------------------------


def sign(secret, body):
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def handle_webhook(provider, body, signature):
    """Verify the signature, then record the payment once. Returns (status, message)."""
    secret = getattr(settings, "PAYMENT_WEBHOOK_SECRETS", {}).get(provider)
    if not secret:
        return 404, "unknown provider"
    if not signature or not hmac.compare_digest(sign(secret, body), signature):
        return 401, "bad signature"
    try:
        data = json.loads(body)
        order = Order.objects.get(ref=data["order_ref"])
        status = data["status"]
        event_id = str(data["event_id"])
        amount, fees = int(data["amount_minor"]), int(data.get("fees_minor", 0))
    except (ValueError, KeyError, Order.DoesNotExist):
        return 400, "bad payload"
    if status != "succeeded":
        return 200, "ignored"
    try:
        _, created = record_payment(
            order, provider=provider, provider_ref=event_id, amount_minor=amount, fees_minor=fees, raw=data
        )
    except BillingError as exc:
        return 409, str(exc)
    return 200, "recorded" if created else "duplicate"


def seed_products():
    Plan.objects.get_or_create(key="subscriber_scope", defaults=dict(name="Subscriber (scope)"))
    Product.objects.get_or_create(
        key="subscription-city-month",
        defaults=dict(
            name="Subscription for a city and list type, 30 days", kind="subscription", price_minor=2900, period_days=30
        ),
    )
    Product.objects.get_or_create(
        key="list-access-30",
        defaults=dict(name="Full access to one list, 30 days", kind="list_access", price_minor=9900, period_days=30),
    )
    Product.objects.get_or_create(
        key="company-page-quarter",
        defaults=dict(name="Company page, 90 days", kind="listing", price_minor=14900, period_days=90),
    )
