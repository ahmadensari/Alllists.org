from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.test import Client

from accounts.roles import grant_role
from billing import services as bs
from billing.models import Product
from billing.reconcile import all_ok, reconcile
from core import clock
from entries.models import CreditEvent
from ledger import services as ledger
from ledger.models import Payout, RatePhase


@pytest.fixture
def world(tree, surgical, users, make_published, db):
    import datetime

    RatePhase.objects.create(name="Phase 1", starts_on=datetime.date(2020, 1, 1), rate_percent=50)
    other = User.objects.create_user("other_adder", "o@x.org", "x")
    make_published("Alpha Works", tree["paris"], phone="0300 000 0101", refresh=False)
    b = make_published("Beta Works", tree["paris"], phone="0300 000 0102", refresh=False)
    CreditEvent.objects.filter(entry=b).update(user=other)
    buyer = User.objects.create_user("buyer", "b@x.org", "x")
    f1 = User.objects.create_user("fin1", "f1@x.org", "x")
    f2 = User.objects.create_user("fin2", "f2@x.org", "x")
    bs.seed_products()
    return dict(adder=users["adder"], other=other, buyer=buyer, f1=f1, f2=f2, surgical=surgical)


def _sell(w, ref, key="list-access-30", when=None):
    order = bs.create_order(
        w["buyer"], Product.objects.get(key=key), scope_path="pk.punjab.sialkot", concept=w["surgical"]
    )
    bs.record_payment(
        order,
        provider="manual",
        provider_ref=ref,
        amount_minor=order.amount_minor,
        fees_minor=250,
        actor=w["f1"],
        now=when,
    )
    return order


def _kyc(w, user):
    ledger.decide_kyc(
        ledger.submit_kyc(user, legal_name="A Person", country_code="PK", method="bank", account="PK00 0000"),
        actor=w["f2"],
        approve=True,
    )


def test_two_payout_cycles_reconcile_to_the_cent(world):
    w = world
    past = clock.now() - timedelta(days=40)
    _sell(w, "P1", when=past)
    _sell(w, "P2", when=past)
    assert all_ok(reconcile())
    ledger.release_holds()
    with pytest.raises(ledger.LedgerError):
        ledger.create_batch(w["f1"])  # nobody has approved payout details yet
    _kyc(w, w["adder"])
    _kyc(w, w["other"])
    batch = ledger.create_batch(w["f1"])
    assert batch.payouts.count() == 2 and batch.total_minor == sum(p.amount_minor for p in batch.payouts.all())
    with pytest.raises(ledger.LedgerError):
        ledger.approve_batch(batch, approver=w["f1"])
    ledger.approve_batch(batch, approver=w["f2"])
    refs = {p.pk: f"BANK-{p.pk}" for p in batch.payouts.all()}
    with pytest.raises(ledger.LedgerError):
        ledger.mark_batch_paid(batch, {})
    ledger.mark_batch_paid(batch, refs)
    assert all_ok(reconcile())
    # cycle two: a new sale, released after its hold, paid in a second batch
    _sell(w, "P3", when=clock.now() - timedelta(days=20))
    ledger.release_holds()
    assert all_ok(reconcile())
    second = ledger.create_batch(w["f1"])
    ledger.approve_batch(second, approver=w["f2"])
    ledger.mark_batch_paid(second, {p.pk: f"BANK2-{p.pk}" for p in second.payouts.all()})
    results = reconcile()
    assert all_ok(results), [r for r in results if not r["ok"]]
    assert Payout.objects.filter(state="paid").count() == 4
    for u in (w["adder"], w["other"]):
        assert ledger.payable_balance(u) == 0 or ledger.payable_balance(u) < ledger.MIN_PAYOUT_MINOR


def test_reconcile_reports_a_difference_instead_of_hiding_it(world):
    from ledger.models import SaleAllocation

    _sell(world, "P9")
    SaleAllocation.objects.update(amount_minor=1)  # a wrong figure in the allocation table
    bad = [r["check"] for r in reconcile() if not r["ok"]]
    assert any("holding" in c for c in bad)


def test_changed_payout_details_need_review_again(world):
    w = world
    _kyc(w, w["adder"])
    assert ledger.kyc_ok(w["adder"])
    ledger.submit_kyc(w["adder"], legal_name="A Person", country_code="PK", method="bank", account="PK99 NEW")
    assert not ledger.kyc_ok(w["adder"])
    prof = w["adder"].payout_profile
    with pytest.raises(ledger.LedgerError):
        ledger.decide_kyc(prof, actor=w["adder"], approve=True)  # nobody approves their own details


def test_payout_details_are_encrypted_at_rest(world):
    from django.db import connection

    _kyc(world, world["adder"])
    with connection.cursor() as cur:
        cur.execute("select legal_name_enc, account_enc from ledger_payoutprofile")
        name, acct = cur.fetchone()
    assert "A Person" not in name and "PK00" not in acct


def test_finance_pages_need_the_right_roles(world):
    w = world
    c = Client()
    c.force_login(w["buyer"])
    assert c.get("/staff/ledger/").status_code in (302, 403)
    grant_role(w["f1"], "finance")
    fc = Client()
    fc.force_login(w["f1"])
    s = fc.session
    s["mfa_ok"] = True
    s.save()
    assert fc.get("/staff/ledger/").status_code == 200
