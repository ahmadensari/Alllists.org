"""Ledger reconciliation (plan 12.5, P5.05). Every figure on the ledger is recomputed from the records that caused it.
A check that does not agree is reported, never silently fixed."""

from django.db.models import Sum

from ledger.models import LedgerAccount, LedgerPosting, Payout, Sale, SaleAllocation
from ledger.services import balance

from .models import Order, Payment


def _acc(kind, currency):
    return sum(balance(a) for a in LedgerAccount.objects.filter(kind=kind, currency=currency))


def reconcile(currency="USD"):
    """Returns a list of dicts {check, expected, actual, ok}. All numbers are minor units."""
    sales = Sale.objects.filter(currency=currency, state="recorded")
    allocs = SaleAllocation.objects.filter(sale__currency=currency, reversed_at__isnull=True)
    paid_out = Payout.objects.filter(currency=currency, state="paid").aggregate(s=Sum("amount_minor"))["s"] or 0
    received = (
        Payment.objects.filter(
            order__currency=currency, order__state=Order.State.FULFILLED, state=Payment.State.SUCCEEDED
        ).aggregate(s=Sum("amount_minor"))["s"]
        or 0
    )
    released = allocs.filter(released_at__isnull=False).aggregate(s=Sum("amount_minor"))["s"] or 0
    held = allocs.filter(released_at__isnull=True).aggregate(s=Sum("amount_minor"))["s"] or 0
    sale_sum = lambda f: sales.aggregate(s=Sum(f))["s"] or 0  # noqa: E731
    checks = [
        (
            "all postings sum to zero",
            0,
            LedgerPosting.objects.filter(currency=currency).aggregate(s=Sum("amount_minor"))["s"] or 0,
        ),
        ("money in clearing equals payments received on live orders", received, _acc("clearing", currency)),
        ("provider fees owed equal fees on live sales", sale_sum("fees_minor"), -_acc("fees", currency)),
        ("tax collected equals tax on live sales", sale_sum("tax_minor"), -_acc("tax", currency)),
        ("contributor money in holding equals unreleased allocations", held, -_acc("holding", currency)),
        ("payable equals released allocations less payouts made", released - paid_out, -_acc("payable", currency)),
        ("payout account equals payouts marked paid", paid_out, -_acc("payout", currency)),
        (
            "platform plus contributors plus fees plus tax equal gross on live sales",
            sale_sum("gross_minor"),
            -_acc("platform", currency) + held + released + sale_sum("fees_minor") + sale_sum("tax_minor"),
        ),
    ]
    return [{"check": c, "expected": e, "actual": a, "ok": e == a} for c, e, a in checks]


def all_ok(results):
    return all(r["ok"] for r in results)
