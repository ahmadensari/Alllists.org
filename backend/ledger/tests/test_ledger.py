import datetime
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.db.utils import IntegrityError, InternalError
from hypothesis import given, settings as hsettings
from hypothesis import strategies as st

from core import clock
from entries import services as es
from ledger import services as ledger
from ledger.models import LedgerAccount, LedgerPosting, LedgerTxn, Payout, RatePhase, Sale

pairs = st.lists(st.tuples(st.integers(1, 6), st.sampled_from([0, 30, 40, 50, 100])), min_size=1, max_size=40)


@given(net=st.integers(0, 10**9), items=pairs)
@hsettings(max_examples=200, deadline=None)
def test_allocation_conserves_every_cent(net, items):
    contrib, platform = ledger.compute_allocation(net, items)
    assert platform >= 0 and all(v > 0 for v in contrib.values())
    assert sum(contrib.values()) + platform == net


@given(net=st.integers(0, 10**9), items=pairs, seed=st.randoms())
@hsettings(max_examples=100, deadline=None)
def test_allocation_does_not_depend_on_entry_order(net, items, seed):
    shuffled = list(items)
    seed.shuffle(shuffled)
    assert ledger.compute_allocation(net, items) == ledger.compute_allocation(net, shuffled)


@given(net=st.integers(0, 10**7), items=pairs)
@hsettings(max_examples=100, deadline=None)
def test_no_contributor_exceeds_their_rate_share(net, items):
    contrib, _ = ledger.compute_allocation(net, items)
    n = len(items)
    for uid, amount in contrib.items():
        ceiling = sum(r for u, r in items if u == uid) * net / (100 * n)
        assert amount <= ceiling + 1


weighted = st.lists(
    st.tuples(st.integers(1, 6), st.sampled_from([0, 30, 40, 50, 100]), st.sampled_from([1, 1.25, 2])),
    min_size=1,
    max_size=30,
)


@given(net=st.integers(0, 10**9), items=weighted)
@hsettings(max_examples=150, deadline=None)
def test_weighted_allocation_conserves_every_cent_and_is_order_free(net, items):
    contrib, platform = ledger.compute_allocation(net, [(u, r, str(w)) for u, r, w in items])
    assert platform >= 0 and sum(contrib.values()) + platform == net
    assert (contrib, platform) == ledger.compute_allocation(net, [(u, r, str(w)) for u, r, w in reversed(items)])


def test_equal_weights_match_the_unweighted_result():
    items = [(1, 50), (1, 50), (2, 40)]
    assert ledger.compute_allocation(9700, items) == ledger.compute_allocation(9700, [(u, r, 1) for u, r in items])


def test_allocation_matches_the_worked_example_in_the_plan():
    # net 97.00, ten verified entries: A has 6 at 50 percent, B has 4 at 40 percent
    items = [(1, 50)] * 6 + [(2, 40)] * 4
    contrib, platform = ledger.compute_allocation(9700, items)
    assert contrib == {1: 2910, 2: 1552} and platform == 9700 - 2910 - 1552 == 5238


def test_rate_must_be_valid_and_empty_goes_to_platform():
    with pytest.raises(ledger.LedgerError):
        ledger.compute_allocation(100, [(1, 120)])
    assert ledger.compute_allocation(100, []) == ({}, 100)


# ---- transactions on PostgreSQL -----------------------------------------------------------------------------------------


def test_unbalanced_transaction_is_refused_before_the_database(db):
    a, b = ledger.account("clearing"), ledger.account("platform")
    with pytest.raises(ledger.LedgerError):
        ledger.post("bad", "adjustment", [(a, 100), (b, -90)])


def test_database_trigger_rejects_unbalanced_postings_even_if_the_service_is_bypassed(pg):
    a = ledger.account("clearing")
    with pytest.raises((IntegrityError, InternalError)), transaction.atomic():
        txn = LedgerTxn.objects.create(idempotency_key="raw", kind="adjustment")
        LedgerPosting.objects.create(txn=txn, account=a, amount_minor=100)
        with connection.cursor() as cur:
            cur.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_ledger_tables_are_append_only(pg):
    a, b = ledger.account("clearing"), ledger.account("platform")
    txn, _ = ledger.post("ok", "adjustment", [(a, 50), (b, -50)])
    for sql in (
        "UPDATE ledger_ledgerposting SET amount_minor = 1",
        "DELETE FROM ledger_ledgertxn",
        "UPDATE ledger_ledgertxn SET memo = 'x'",
        "DELETE FROM ledger_ledgerposting",
    ):
        with pytest.raises((IntegrityError, InternalError)), transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(sql)
    assert LedgerPosting.objects.count() == 2


def test_post_is_idempotent(db):
    a, b = ledger.account("clearing"), ledger.account("platform")
    t1, c1 = ledger.post("k1", "adjustment", [(a, 10), (b, -10)])
    t2, c2 = ledger.post("k1", "adjustment", [(a, 10), (b, -10)])
    assert t1.pk == t2.pk and c1 and not c2 and LedgerPosting.objects.count() == 2


# ---- rate phases ---------------------------------------------------------------------------------------------------------


def phases():
    today = clock.today()
    p1 = RatePhase.objects.create(
        name="Phase 1",
        starts_on=today - timedelta(days=400),
        ends_on=today + timedelta(days=100),
        rate_percent=50,
        cap_months=36,
    )
    p2 = RatePhase.objects.create(name="Phase 2", starts_on=today + timedelta(days=101), rate_percent=40, cap_months=36)
    p3 = RatePhase.objects.create(name="Phase 3", starts_on=today + timedelta(days=900), rate_percent=30, cap_months=36)
    return p1, p2, p3


def test_phase_is_locked_when_first_published_and_later_phases_do_not_touch_it(entry, users, db):
    p1, p2, p3 = phases()
    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    entry.refresh_from_db()
    assert entry.phase_id == p1.pk
    p1.ends_on = clock.today() - timedelta(days=1)  # the phase ends; the lock stays
    p1.save()
    assert ledger.current_phase() is None  # the phase ended; the entry keeps its lock
    assert ledger.lock_phase(entry) == p1.pk
    credit = entry.credit_events.get(kind="added")
    assert ledger.rate_for(entry, credit.created_at) == 50


def test_rate_drops_to_the_lowest_after_the_cap(entry, users, db):
    p1, p2, p3 = phases()
    entry.phase_id = p1.pk
    entry.save()
    old = clock.now() - timedelta(days=36 * 31)
    assert ledger.rate_for(entry, old) == 30
    assert ledger.rate_for(entry, clock.now() - timedelta(days=30)) == 50
    assert ledger.months_between(datetime.date(2024, 1, 31), datetime.date(2024, 3, 1)) == 1


def test_entry_without_a_phase_earns_the_lowest_rate(entry, users, db):
    phases()
    assert ledger.rate_for(entry, clock.now()) == 30


# ---- sales, holds, refunds, payouts ---------------------------------------------------------------------------------------


@pytest.fixture
def scene(tree, surgical, users, make_published, db):
    phases()
    other = User.objects.create_user("other_adder", "o@x.org", "x")
    e1 = make_published("Alpha Works", tree["paris"], phone="0300 000 0101", refresh=False)
    e2 = make_published("Beta Works", tree["paris"], phone="0300 000 0102", refresh=False)
    from entries.models import CreditEvent

    CreditEvent.objects.filter(entry=e2).update(user=other)
    e3 = es.create_entry(
        name="Gamma Self",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        created_via="self",
        website="https://g.example.org",
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    es.record_verification(
        e3, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    return dict(e1=e1, e2=e2, e3=e3, adder=users["adder"], other=other, surgical=surgical)


def approve_kyc(user, reviewer):
    prof = ledger.submit_kyc(user, legal_name="A Person", country_code="PK", method="bank", account="PK00 TEST 0000")
    ledger.decide_kyc(prof, actor=reviewer, approve=True)


def balances():
    return {(a.kind, a.user_id): ledger.balance(a) for a in LedgerAccount.objects.all()}


def test_list_sale_pays_only_verified_eligible_entries_and_every_account_balances(scene):
    s = scene
    sale = ledger.record_sale(
        "O1", "list", gross=10000, fees=300, scope_path="pk.punjab.sialkot", concept=s["surgical"]
    )
    assert sale.net_minor == 9700
    allocs = {a.user_id: a.amount_minor for a in sale.allocations.all()}
    # two eligible entries (Gamma is self-listed and sits outside the denominator): slice 4850, phase 50 percent
    assert allocs == {s["adder"].pk: 2425, s["other"].pk: 2425}
    assert sum(b for b in balances().values()) == 0
    assert balances()[("platform", None)] == -(9700 - 4850) and balances()[("clearing", None)] == 10000
    assert sale.allocations.first().entry_count == 1


def test_non_list_sales_are_platform_revenue(scene):
    sale = ledger.record_sale("O2", "rank", gross=2900)
    assert not sale.allocations.exists() and balances()[("platform", None)] == -2900


def test_subscription_sale_pays_scope_entries_with_a_freshness_bonus(scene):
    s = scene
    # Alpha was just re-verified; make Beta's last check old so only Alpha gets the 0.25 bonus
    s["e2"].__class__.objects.filter(pk=s["e2"].pk).update(last_verified_at=clock.now() - timedelta(days=200))
    sale = ledger.record_sale("S1", "subscription", gross=2900, scope_path="pk.punjab.sialkot", concept=s["surgical"])
    allocs = {a.user_id: a.amount_minor for a in sale.allocations.all()}
    # weights 1.25 and 1.00 over net 2900: 1611.11 and 1288.89, each at 50 percent
    assert allocs == {s["adder"].pk: 806, s["other"].pk: 644}
    assert sum(balances().values()) == 0


def test_sale_is_idempotent(scene):
    a = ledger.record_sale("O3", "list", gross=5000, scope_path="pk.punjab.sialkot", concept=scene["surgical"])
    b = ledger.record_sale("O3", "list", gross=5000, scope_path="pk.punjab.sialkot", concept=scene["surgical"])
    assert a.pk == b.pk and Sale.objects.count() == 1 and sum(balances().values()) == 0


def test_negative_amounts_and_fees_over_gross_are_refused(scene):
    with pytest.raises(ledger.LedgerError):
        ledger.record_sale("O4", "list", gross=100, fees=200)
    with pytest.raises(ledger.LedgerError):
        ledger.record_sale("O5", "list", gross=-5)


def test_hold_then_release_then_refund_exactly_reverses(scene):
    s = scene
    start = clock.now()
    sale = ledger.record_sale(
        "O6", "list", gross=10000, scope_path="pk.punjab.sialkot", concept=s["surgical"], now=start
    )
    assert ledger.release_holds(start + timedelta(days=13)) == 0
    assert ledger.release_holds(start + timedelta(days=15)) == 2
    assert ledger.release_holds(start + timedelta(days=16)) == 0
    assert ledger.payable_balance(s["adder"]) == 2500
    ledger.refund_sale(sale)
    assert all(v == 0 for v in balances().values())
    assert sale.allocations.filter(reversed_at__isnull=False).count() == 2
    ledger.refund_sale(sale)  # a second refund changes nothing
    assert all(v == 0 for v in balances().values())


def test_payout_needs_a_second_person_and_never_exceeds_payable(scene):
    s = scene
    start = clock.now() - timedelta(days=30)
    ledger.record_sale("O7", "list", gross=100000, scope_path="pk.punjab.sialkot", concept=s["surgical"], now=start)
    ledger.release_holds()
    f1 = User.objects.create_user("fin1", "f1@x.org", "x")
    f2 = User.objects.create_user("fin2", "f2@x.org", "x")
    owed = ledger.payable_balance(s["adder"])
    assert owed == 25000
    with pytest.raises(ledger.LedgerError, match="not been approved"):
        ledger.create_payout(s["adder"], creator=f1, amount_minor=10000)
    approve_kyc(s["adder"], f2)
    with pytest.raises(ledger.LedgerError):
        ledger.create_payout(s["adder"], creator=f1, amount_minor=owed + 1)
    with pytest.raises(ledger.LedgerError):
        ledger.create_payout(s["adder"], creator=f1, amount_minor=100)  # below the minimum
    p = ledger.create_payout(s["adder"], creator=f1, amount_minor=10000)
    assert ledger.payable_balance(s["adder"]) == 15000  # reserved while pending
    with pytest.raises(ledger.LedgerError):
        ledger.approve_payout(p, approver=f1)
    with pytest.raises(ledger.LedgerError):
        ledger.mark_paid(p, external_ref="X")
    ledger.approve_payout(p, approver=f2)
    ledger.mark_paid(p, external_ref="BANK-1")
    p.refresh_from_db()
    assert p.state == Payout.State.PAID and ledger.payable_balance(s["adder"]) == 15000
    assert sum(balances().values()) == 0 and balances()[("payout", None)] == -10000


def test_payout_total_never_exceeds_collections(scene):
    s = scene
    ledger.record_sale(
        "O8",
        "list",
        gross=20000,
        scope_path="pk.punjab.sialkot",
        concept=s["surgical"],
        now=clock.now() - timedelta(days=30),
    )
    ledger.release_holds()
    paid = 0
    f1 = User.objects.create_user("fa", "a@x.org", "x")
    f2 = User.objects.create_user("fb", "b@x.org", "x")
    for user in (s["adder"], s["other"]):
        approve_kyc(user, f2)
        p = ledger.create_payout(user, creator=f1)
        ledger.approve_payout(p, approver=f2)
        ledger.mark_paid(p, external_ref=f"B-{user.pk}")
        paid += p.amount_minor
    assert paid <= 20000 and ledger.payable_balance(s["adder"]) == 0


def test_cents_are_conserved_for_awkward_amounts(scene):
    for i, gross in enumerate([1, 7, 99, 101, 12345, 99999]):
        sale = ledger.record_sale(
            f"C{i}", "list", gross=gross, scope_path="pk.punjab.sialkot", concept=scene["surgical"]
        )
        pool = sum(a.amount_minor for a in sale.allocations.all())
        platform = -sum(p.amount_minor for p in sale.txn.postings.all() if p.account.kind == "platform")
        assert pool + platform == sale.net_minor
    assert sum(balances().values()) == 0
