"""Ledger service (plan 12). Every money movement is a balanced, idempotent transaction; corrections are reversals."""

from collections import defaultdict
from datetime import timedelta
from fractions import Fraction
from math import floor

from django.conf import settings
from django.db import transaction
from django.db.models import Sum

from core import clock
from core.models import audit
from entries.models import CreditEvent, Entry

from .models import LedgerAccount, LedgerPosting, LedgerTxn, Payout, RatePhase, Sale, SaleAllocation

MIN_PAYOUT_MINOR = 500
LOWEST_RATE_DEFAULT = 30


class LedgerError(ValueError):
    pass


# ---- accounts and postings --------------------------------------------------------------------------------------


def account(kind, user=None, currency="USD"):
    acc, _ = LedgerAccount.objects.get_or_create(kind=kind, user=user, currency=currency)
    return acc


def balance(acc):
    return LedgerPosting.objects.filter(account=acc).aggregate(s=Sum("amount_minor"))["s"] or 0


@transaction.atomic
def post(key, kind, postings, *, ref="", memo="", reverses=None, now=None):
    """Create one balanced transaction. `postings` is a list of (account, signed minor units). Idempotent on `key`."""
    existing = LedgerTxn.objects.filter(idempotency_key=key).first()
    if existing:
        return existing, False
    sums = defaultdict(int)
    for acc, amount in postings:
        sums[acc.currency] += amount
    if any(v != 0 for v in sums.values()):
        raise LedgerError(f"transaction {key} does not balance: {dict(sums)}")
    txn = LedgerTxn.objects.create(
        idempotency_key=key, kind=kind, ref=ref, memo=memo[:200], reverses=reverses, ts=now or clock.now()
    )
    LedgerPosting.objects.bulk_create(
        [LedgerPosting(txn=txn, account=a, amount_minor=m, currency=a.currency) for a, m in postings if m != 0]
    )
    return txn, True


# ---- rate phases (rule R11) ---------------------------------------------------------------------------------------


def current_phase(today=None):
    today = today or clock.today()
    return RatePhase.objects.filter(starts_on__lte=today).exclude(ends_on__lt=today).order_by("-starts_on").first()


def lowest_rate():
    rates = list(RatePhase.objects.values_list("rate_percent", flat=True))
    return min(rates) if rates else LOWEST_RATE_DEFAULT


def lock_phase(entry):
    """Set the entry's phase once, the first time it is accepted. Later phase changes never touch it."""
    if entry.phase_id is None:
        phase = current_phase()
        if phase:
            entry.phase_id = phase.pk
            entry.save(update_fields=["phase_id"])
    return entry.phase_id


def months_between(start, end):
    return (end.year - start.year) * 12 + (end.month - start.month) - (1 if end.day < start.day else 0)


def rate_for(entry, credit_created, today=None):
    """The contributor rate for an entry: its locked phase, dropping to the lowest rate after the cap (rule R12)."""
    today = today or clock.today()
    phase = RatePhase.objects.filter(pk=entry.phase_id).first() if entry.phase_id else None
    if phase is None:
        return lowest_rate()
    if (
        months_between(credit_created.date() if hasattr(credit_created, "date") else credit_created, today)
        >= phase.cap_months
    ):
        return min(phase.rate_percent, lowest_rate())
    return phase.rate_percent


# ---- allocation (pure function, property-tested) ---------------------------------------------------------------------


def compute_allocation(net_minor, items):
    """Split `net_minor` equally across the entries in `items` [(user_id, rate_percent)], each earning slice times its
    rate. Returns ({user_id: minor}, platform_minor). Largest remainder keeps every cent: contributors plus platform
    equal `net_minor` exactly."""
    if net_minor < 0:
        raise LedgerError("net must not be negative")
    if not items:
        return {}, net_minor
    slice_ = Fraction(net_minor, len(items))
    exact = defaultdict(Fraction)
    for user_id, rate in items:
        if not 0 <= rate <= 100:
            raise LedgerError("rate out of range")
        exact[user_id] += slice_ * Fraction(rate, 100)
    pool = floor(sum(exact.values()))
    floors = {u: floor(v) for u, v in exact.items()}
    leftover = pool - sum(floors.values())
    for u in sorted(exact, key=lambda k: (-(exact[k] - floors[k]), k))[:leftover]:
        floors[u] += 1
    return {u: v for u, v in floors.items() if v > 0}, net_minor - sum(floors.values())


def allocation_items(scope_path, concept, now=None):
    """[(user_id, rate_percent, entry)] for the entries a list sale pays: published, checked by a person (unexpired),
    with a payout-eligible credit (rule R09). Self-listed, agent and import-only entries are not in the denominator."""
    from analytics.rollups import descendant_concept_ids

    now = now or clock.now()
    qs = Entry.objects.filter(publish_state="published", deleted_at__isnull=True, merged_into__isnull=True)
    if scope_path:
        qs = qs.filter(place_path__startswith=scope_path)
        qs = [e for e in qs if e.place_path == scope_path or e.place_path.startswith(scope_path + ".")]
    else:
        qs = list(qs)
    if concept is not None:
        ids = set(descendant_concept_ids(concept.pk))
        qs = [e for e in qs if e.primary_concept_id in ids]
    out = []
    for e in qs:
        levels = {
            v.level
            for v in e.verification_current.all()
            if v.state == "verified" and v.expires_at and v.expires_at > now
        }
        if not levels & {"surveyor", "owner"}:
            continue
        credit = (
            CreditEvent.objects.filter(entry=e, kind="added", eligible=True, user__isnull=False)
            .order_by("created_at", "id")
            .first()
        )
        if credit is None:
            continue
        out.append((credit.user_id, rate_for(e, credit.created_at, now.date()), e))
    return out


# ---- sales ----------------------------------------------------------------------------------------------------------


@transaction.atomic
def record_sale(order_ref, kind, *, gross, fees=0, tax=0, currency="USD", scope_path="", concept=None, now=None):
    """Record a paid sale. Only list sales feed the contributor pool; everything else is platform revenue (plan 12.2)."""
    existing = Sale.objects.filter(order_ref=order_ref).first()
    if existing:
        return existing
    now = now or clock.now()
    net = gross - fees - tax
    if min(gross, fees, tax) < 0 or net < 0:
        raise LedgerError("amounts must not be negative and fees plus tax cannot exceed the gross amount")
    alloc, platform = {}, net
    counts = {}
    if kind == Sale.Kind.LIST:
        items = allocation_items(scope_path, concept, now)
        alloc, platform = compute_allocation(net, [(u, r) for u, r, _ in items])
        for u, _, _ in items:
            counts[u] = counts.get(u, 0) + 1
    elif kind == Sale.Kind.OUTREACH and settings.OUTREACH_SHARE_PERCENT:
        # contributors share a fixed percentage of outreach revenue, split equally across the eligible entries (F7)
        items = allocation_items(scope_path, concept, now)
        pool = floor(Fraction(net) * Fraction(str(settings.OUTREACH_SHARE_PERCENT)) / 100)
        alloc, _ = compute_allocation(pool, [(u, 100) for u, _, _ in items])
        platform = net - sum(alloc.values())
        for u, _, _ in items:
            counts[u] = counts.get(u, 0) + 1
    postings = [(account("clearing", None, currency), gross)]
    if fees:
        postings.append((account("fees", None, currency), -fees))
    if tax:
        postings.append((account("tax", None, currency), -tax))
    from django.contrib.auth import get_user_model

    users = {u.pk: u for u in get_user_model().objects.filter(pk__in=alloc)}
    for uid, amount in alloc.items():
        postings.append((account("holding", users[uid], currency), -amount))
    if platform:
        postings.append((account("platform", None, currency), -platform))
    txn, _ = post(f"sale:{order_ref}", "sale", postings, ref=order_ref, now=now)
    sale = Sale.objects.create(
        order_ref=order_ref,
        kind=kind,
        scope_path=scope_path,
        concept=concept,
        currency=currency,
        gross_minor=gross,
        fees_minor=fees,
        tax_minor=tax,
        net_minor=net,
        txn=txn,
        ts=now,
    )
    for uid, amount in alloc.items():
        SaleAllocation.objects.create(
            sale=sale,
            user=users[uid],
            entry_count=counts[uid],
            amount_minor=amount,
            hold_until=now + timedelta(days=settings.REFUND_HOLD_DAYS),
        )
    audit(
        "sale.record",
        object_type="sale",
        object_uid=order_ref,
        payload={"kind": kind, "net": net, "pool": net - platform},
    )
    return sale


@transaction.atomic
def release_holds(now=None):
    """Move allocations past the refund hold from holding to payable. Returns how many were released."""
    now = now or clock.now()
    n = 0
    for a in (
        SaleAllocation.objects.select_for_update()
        .filter(released_at__isnull=True, reversed_at__isnull=True, hold_until__lte=now)
        .select_related("sale", "user")
    ):
        cur = a.sale.currency
        post(
            f"release:{a.pk}",
            "release",
            [(account("holding", a.user, cur), a.amount_minor), (account("payable", a.user, cur), -a.amount_minor)],
            ref=a.sale.order_ref,
            now=now,
        )
        a.released_at = now
        a.save(update_fields=["released_at"])
        n += 1
    return n


@transaction.atomic
def refund_sale(sale, *, actor=None, now=None):
    """Reverse a sale exactly: the sale and any releases are negated, so every account returns to where it was."""
    if sale.state == Sale.State.REFUNDED:
        return sale
    now = now or clock.now()
    for a in sale.allocations.filter(released_at__isnull=False, reversed_at__isnull=True).select_related("user"):
        rel = LedgerTxn.objects.get(idempotency_key=f"release:{a.pk}")
        post(
            f"unrelease:{a.pk}",
            "refund",
            [(p.account, -p.amount_minor) for p in rel.postings.all()],
            reverses=rel,
            now=now,
        )
    post(
        f"refund:{sale.pk}",
        "refund",
        [(p.account, -p.amount_minor) for p in sale.txn.postings.all()],
        reverses=sale.txn,
        ref=sale.order_ref,
        now=now,
    )
    sale.allocations.update(reversed_at=now)
    sale.state = Sale.State.REFUNDED
    sale.save(update_fields=["state"])
    audit("sale.refund", actor=actor, object_type="sale", object_uid=sale.order_ref)
    return sale


# ---- payouts (two-person rule) -----------------------------------------------------------------------------------------


def payable_balance(user, currency="USD"):
    """Released money owed to the user, minus payouts already asked for."""
    acc = LedgerAccount.objects.filter(kind="payable", user=user, currency=currency).first()
    owed = -balance(acc) if acc else 0
    reserved = (
        Payout.objects.filter(user=user, currency=currency, state__in=["pending", "approved"]).aggregate(
            s=Sum("amount_minor")
        )["s"]
        or 0
    )
    return owed - reserved


@transaction.atomic
def create_payout(user, *, creator, amount_minor=None, method="", currency="USD"):
    avail = payable_balance(user, currency)
    amount = avail if amount_minor is None else amount_minor
    if amount <= 0 or amount > avail:
        raise LedgerError("amount exceeds what is payable")
    if amount < MIN_PAYOUT_MINOR:
        raise LedgerError("below the minimum payout")
    p = Payout.objects.create(user=user, currency=currency, amount_minor=amount, method=method, created_by=creator)
    audit("payout.create", actor=creator, object_type="payout", object_uid=str(p.pk), payload={"amount": amount})
    return p


@transaction.atomic
def approve_payout(payout, *, approver):
    """The approver must differ from the creator (rule: separation of duties)."""
    if payout.state != Payout.State.PENDING:
        raise LedgerError("payout is not pending")
    if approver.pk == payout.created_by_id:
        raise LedgerError("the person who created a payout cannot approve it")
    payout.state, payout.approved_by = Payout.State.APPROVED, approver
    payout.save(update_fields=["state", "approved_by"])
    audit("payout.approve", actor=approver, object_type="payout", object_uid=str(payout.pk))
    return payout


@transaction.atomic
def mark_paid(payout, *, external_ref, now=None):
    if payout.state != Payout.State.APPROVED:
        raise LedgerError("payout must be approved first")
    cur = payout.currency
    txn, _ = post(
        f"payout:{payout.pk}",
        "payout",
        [
            (account("payable", payout.user, cur), payout.amount_minor),
            (account("payout", None, cur), -payout.amount_minor),
        ],
        ref=external_ref,
        now=now,
    )
    payout.state, payout.external_ref, payout.txn = Payout.State.PAID, external_ref[:80], txn
    payout.save(update_fields=["state", "external_ref", "txn"])
    audit("payout.paid", object_type="payout", object_uid=str(payout.pk), payload={"ref": external_ref})
    return payout
