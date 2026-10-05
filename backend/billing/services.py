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
from places.models import Place

from .models import Invoice, Order, Payment, Product

KIND_TO_SALE = {
    "subscription": Sale.Kind.SUBSCRIPTION,
    "list_access": Sale.Kind.LIST,
    "listing": Sale.Kind.LISTING,
    "rank": Sale.Kind.RANK,
    "outreach": Sale.Kind.OUTREACH,
    "extract": Sale.Kind.EXTRACT,
    "ad": Sale.Kind.AD,
}


class BillingError(ValueError):
    pass


def scoped_price(base_minor, scope_path, concept):
    """The listed price is for one city and one list type. A region or a country costs more, and so does every list type
    in a place (multipliers in settings), so a cheap order cannot unlock much more than was paid for."""
    depth = min(len(scope_path.split(".")), 3)
    mult = Decimal(str(settings.SUBSCRIPTION_SCOPE_MULTIPLIER.get(depth, 1)))
    if concept is None:
        mult *= Decimal(str(settings.SUBSCRIPTION_ANY_TYPE_MULTIPLIER))
    return int((Decimal(base_minor) * mult).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def tax_rate_for(country_code):
    return str(getattr(settings, "TAX_RATES", {}).get((country_code or "").upper(), "0"))


def tax_for(country_code, amount_minor):
    """Tax in minor units from a per-country percentage in settings; none when unconfigured."""
    rate = Decimal(str(getattr(settings, "TAX_RATES", {}).get((country_code or "").upper(), "0")))
    return int((Decimal(amount_minor) * rate / Decimal(100)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def new_ref():
    from core.ulid import new_ulid

    return "O" + new_ulid()[:12]


@transaction.atomic
def create_order(buyer, product, *, scope_path="", concept=None, entry=None, campaign=None, ad=None, billing=None):
    if not product.active:
        raise BillingError("this product is not on sale")
    price = product.price_minor
    if product.kind == Product.Kind.SUBSCRIPTION:
        if not scope_path:
            raise BillingError("choose a place for the subscription; the whole world is not sold at the city price")
        price = scoped_price(product.price_minor, scope_path, concept)
    if product.kind == Product.Kind.LISTING:
        if entry is None or not es.company_page_allowed(entry):
            raise BillingError("a company page needs an eligible entry")
        if not es.is_owner(entry, buyer):
            raise BillingError("only the owner can buy a company page")
    elif product.kind == Product.Kind.LIST_ACCESS and (concept is None or not scope_path):
        raise BillingError("choose a place and a list type")
    elif product.kind == Product.Kind.OUTREACH:
        if campaign is None or campaign.buyer_id != buyer.pk or campaign.status not in ("pending", "approved"):
            raise BillingError("choose one of your pending campaigns")
        price, scope_path, concept = campaign.budget_minor, campaign.scope_path, campaign.concept
    elif product.kind == Product.Kind.RANK:
        from access import placements as pl

        if entry is None or concept is None or not es.is_owner(entry, buyer):
            raise BillingError("only the owner can sponsor an entry, on a chosen list type")
        place = Place.objects.filter(path=scope_path, status="active").first()
        if place is None:
            raise BillingError("choose a place")
        try:
            pl.check_capacity(entry, place, concept, months=max(product.period_days // 30, 1))
        except pl.PlacementError as exc:
            raise BillingError(str(exc)) from exc
    elif product.kind == Product.Kind.AD:
        if ad is None or ad.advertiser_id != buyer.pk or ad.order_ref:
            raise BillingError("choose one of your submitted ads")
        entry = ad.entry
    country = scope_path.split(".")[0] if scope_path else (entry.country_code if entry else "")
    tax = tax_for(country, price)
    order = Order.objects.create(
        buyer=buyer,
        product=product,
        currency=product.currency,
        amount_minor=price + tax,
        tax_minor=tax,
        scope_path=scope_path,
        concept=concept,
        entry=entry,
        ref=new_ref(),
        campaign_id=campaign.pk if campaign else None,
        ad_id=ad.pk if ad else None,
        tax_rate=tax_rate_for(country),
        billing={k: str(v)[:200] for k, v in (billing or {}).items() if k in ("name", "address", "tax_id")},
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
    elif p.kind == Product.Kind.OUTREACH:
        from outreach.models import Campaign

        Campaign.objects.filter(pk=order.campaign_id).update(funded=True)
    elif p.kind == Product.Kind.RANK:
        from access import placements as pl

        pl.create_placement(
            order.entry,
            Place.objects.get(path=order.scope_path),
            order.concept,
            months=max(p.period_days // 30, 1),
            price_minor=order.amount_minor - order.tax_minor,
            currency=order.currency,
            order_ref=order.ref,
            now=now,
        )
    elif p.kind == Product.Kind.AD:
        from datetime import timedelta

        from access.models import Ad

        Ad.objects.filter(pk=order.ad_id).update(
            order_ref=order.ref, starts_at=now, ends_at=now + timedelta(days=p.period_days)
        )
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
    issue_invoice(order, now=now)


def next_invoice_number(year):
    from .models import InvoiceCounter

    row, _ = InvoiceCounter.objects.select_for_update().get_or_create(year=year)
    row.last += 1
    row.save(update_fields=["last"])
    return f"AL-{year}-{row.last:06d}"


def _seller():
    return dict(getattr(settings, "COMPANY_DETAILS", {}))


def _buyer(order):
    b = dict(order.billing or {})
    b.setdefault("name", order.buyer.get_full_name() or order.buyer.username)
    return b


@transaction.atomic
def issue_invoice(order, *, now=None):
    """One numbered invoice per order, with the tax rate the order was priced at. Safe to call twice."""
    existing = order.invoices.filter(kind="invoice").first()
    if existing:
        return existing
    now = now or clock.now()
    net = order.amount_minor - order.tax_minor
    lines = [{"item": order.product.name, "amount_minor": net}]
    if order.tax_minor:
        lines.append({"item": f"Tax {order.tax_rate}%", "amount_minor": order.tax_minor})
    return Invoice.objects.create(
        number=next_invoice_number(now.year),
        order=order,
        issued_at=now,
        currency=order.currency,
        seller=_seller(),
        buyer=_buyer(order),
        tax_rate=order.tax_rate,
        lines=lines,
    )


@transaction.atomic
def issue_credit_note(order, *, now=None):
    """A refund never edits the invoice; it issues a numbered credit note with the same lines, negated."""
    now = now or clock.now()
    inv = order.invoices.filter(kind="invoice").first()
    if inv is None or order.invoices.filter(kind="credit_note").exists():
        return None
    return Invoice.objects.create(
        number=next_invoice_number(now.year),
        kind="credit_note",
        credit_for=inv,
        order=order,
        issued_at=now,
        currency=inv.currency,
        seller=inv.seller,
        buyer=inv.buyer,
        tax_rate=inv.tax_rate,
        lines=[{**ln, "amount_minor": -ln["amount_minor"]} for ln in inv.lines],
    )


@transaction.atomic
def refund_order(order, *, actor):
    if order.state != Order.State.FULFILLED:
        raise BillingError("only a fulfilled order can be refunded")
    sale = Sale.objects.get(order_ref=order.ref)
    ledger.refund_sale(sale, actor=actor)
    Entitlement.objects.filter(source__in=[f"order:{order.ref}"]).update(revoked_at=clock.now())
    from access.models import Ad, Placement

    Placement.objects.filter(order_ref=order.ref).update(state="cancelled")
    Ad.objects.filter(order_ref=order.ref).update(state="ended")
    Entitlement.objects.filter(
        source__startswith="subscription:", user=order.buyer, valid_from__gte=order.created_at
    ).update(revoked_at=clock.now())
    order.state = Order.State.REFUNDED
    order.save(update_fields=["state"])
    order.payments.update(state=Payment.State.REFUNDED)
    issue_credit_note(order)
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
    Product.objects.get_or_create(
        key="extract-custom",
        defaults=dict(name="Custom data extract (made by staff)", kind="extract", price_minor=100000, period_days=0),
    )
    Product.objects.get_or_create(
        key="statistics-report",
        defaults=dict(name="Statistics report (aggregates only)", kind="extract", price_minor=25000, period_days=0),
    )
    Product.objects.get_or_create(
        key="rank-city-month",
        defaults=dict(name="Sponsored slot on a list, 30 days", kind="rank", price_minor=19900, period_days=30),
    )
    Product.objects.get_or_create(
        key="ad-month",
        defaults=dict(name="Text ad for free viewers, 30 days", kind="ad", price_minor=4900, period_days=30),
    )
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
