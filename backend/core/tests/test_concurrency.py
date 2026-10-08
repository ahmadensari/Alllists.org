"""Things that must hold when two requests arrive at the same moment: money, payments, tasks, counters, numbers.
Each test starts real threads on real database connections (PostgreSQL), releases them together, and checks that the
promise held."""

import datetime
import threading
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.db import connections

pytestmark = pytest.mark.django_db(transaction=True)

PW = "Correct-horse-battery-9"


def race(n, fn):
    """Run fn(i) in n threads at once. Returns (results, errors)."""
    barrier, results, errors = threading.Barrier(n), [None] * n, [None] * n

    def work(i):
        try:
            barrier.wait(timeout=20)
            results[i] = fn(i)
        except Exception as exc:  # noqa: BLE001
            errors[i] = exc
        finally:
            connections.close_all()

    threads = [threading.Thread(target=work, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)
    return results, errors


@pytest.fixture
def shop(tree, surgical, users, make_published):
    from ledger.models import RatePhase

    RatePhase.objects.create(name="P1", starts_on=datetime.date(2020, 1, 1), rate_percent=50)
    e = make_published("Raced Works", tree["paris"], phone="0300 555 0001")
    return e


def test_one_sale_per_order_however_many_times_it_is_recorded_at_once(shop, surgical):
    from ledger import services as ledger
    from ledger.models import Sale

    results, errors = race(
        8, lambda i: ledger.record_sale("RACE1", "list", gross=10000, scope_path="pk", concept=surgical).pk
    )
    assert [e for e in errors if e] == [], errors
    assert len(set(results)) == 1 and Sale.objects.count() == 1
    from ledger.models import LedgerPosting
    from django.db.models import Sum

    assert (LedgerPosting.objects.aggregate(s=Sum("amount_minor"))["s"] or 0) == 0


def test_one_order_is_paid_and_fulfilled_once_even_with_different_payment_references(shop, surgical, users):
    from access.models import Entitlement
    from billing import services as bs
    from billing.models import Payment, Product
    from ledger.models import Sale

    bs.seed_products()
    buyer = User.objects.create_user("racebuyer", "rb@x.org", PW)
    order = bs.create_order(buyer, Product.objects.get(key="list-access-30"), scope_path="pk", concept=surgical)

    def pay(i):
        from billing.models import Order

        o = Order.objects.get(pk=order.pk)
        return bs.record_payment(o, provider="gateway", provider_ref=f"REF-{i}", amount_minor=o.amount_minor)[1]

    results, errors = race(6, pay)
    assert sum(1 for r in results if r) == 1, (results, errors)  # exactly one thread recorded the payment
    assert all(isinstance(e, bs.BillingError) for e in errors if e), errors
    assert Payment.objects.filter(order=order).count() == 1
    assert Sale.objects.filter(order_ref=order.ref).count() == 1
    assert Entitlement.objects.filter(user=buyer).count() == 1  # not six free months


def test_the_same_payment_reference_arriving_twice_at_once_counts_once(shop, surgical):
    from billing import services as bs
    from billing.models import Order, Payment, Product

    bs.seed_products()
    buyer = User.objects.create_user("racebuyer2", "rb2@x.org", PW)
    order = bs.create_order(buyer, Product.objects.get(key="list-access-30"), scope_path="pk", concept=surgical)

    def pay(i):
        o = Order.objects.get(pk=order.pk)
        return bs.record_payment(o, provider="gateway", provider_ref="SAME", amount_minor=o.amount_minor)[1]

    results, errors = race(6, pay)
    assert [e for e in errors if e and not isinstance(e, bs.BillingError)] == [], errors
    assert Payment.objects.filter(order=order).count() == 1


def test_two_surveyors_never_get_the_same_task(tree, surgical, users, make_published):
    from volunteers import services as vs
    from entries import services as es

    surveyors = [User.objects.create_user(f"sv{i}", f"sv{i}@x.org", PW) for i in range(5)]
    for i in range(5):
        e = es.create_entry(
            name=f"Task Works {i}",
            place=tree["paris"],
            primary_concept=surgical,
            created_by=users["adder"],
            addons={"business_type": "trader", "product_categories": ["x"]},
        )
        vs.queue_verification(e)
    results, errors = race(5, lambda i: (lambda t: t.pk if t else None)(vs.take_next_task(surveyors[i])))
    assert [e for e in errors if e] == [], errors
    got = [r for r in results if r]
    assert len(got) == 5 and len(set(got)) == 5


def test_the_quota_counter_is_exact_under_load(db):
    from access import quotas

    results, errors = race(10, lambda i: [quotas.hit("subject-x", "fragments") for _ in range(5)][-1])
    assert [e for e in errors if e] == [], errors
    assert quotas.current("subject-x", "fragments") == 50


def test_invoice_numbers_are_unique_and_gap_free_under_load(shop, surgical):
    from billing import services as bs
    from billing.models import Invoice, Order, Product

    bs.seed_products()
    buyer = User.objects.create_user("invbuyer", "ib@x.org", PW)
    prod = Product.objects.get(key="list-access-30")
    orders = [bs.create_order(buyer, prod, scope_path="pk", concept=surgical) for _ in range(6)]

    def pay(i):
        o = Order.objects.get(pk=orders[i].pk)
        return bs.record_payment(o, provider="manual", provider_ref=f"INV-{i}", amount_minor=o.amount_minor)[1]

    results, errors = race(6, pay)
    assert [e for e in errors if e] == [], errors
    nums = sorted(Invoice.objects.values_list("number", flat=True))
    assert len(nums) == 6 and len(set(nums)) == 6
    assert [int(n.rsplit("-", 1)[1]) for n in nums] == list(range(1, 7))  # no gaps


def test_two_payouts_asked_at_once_cannot_exceed_what_is_payable(shop, surgical, users):
    from core import clock
    from ledger import services as ledger
    from ledger.models import Payout

    worker = users["adder"]
    fin = User.objects.create_user("racefin", "rf@x.org", PW)
    rev = User.objects.create_user("racerev", "rr@x.org", PW)
    ledger.record_sale(
        "RP1", "list", gross=100000, scope_path="pk", concept=surgical, now=clock.now() - timedelta(days=30)
    )
    ledger.release_holds()
    ledger.decide_kyc(
        ledger.submit_kyc(worker, legal_name="W", country_code="PK", method="bank", account="PK1"),
        actor=rev,
        approve=True,
    )
    owed = ledger.payable_balance(worker)
    assert owed == 50000

    def ask(i):
        w = User.objects.get(pk=worker.pk)
        return ledger.create_payout(w, creator=User.objects.get(pk=fin.pk), amount_minor=40000).pk

    results, errors = race(4, ask)
    made = Payout.objects.filter(user=worker).count()
    assert made == 1, (made, results, errors)  # 4 x 40000 would be 160000 against 50000 payable
    assert ledger.payable_balance(worker) == 10000
