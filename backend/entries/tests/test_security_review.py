"""Regression tests for the findings of the branch security review (self-claim, entity type, scope price, payout
details swap, reply-to validation)."""

import pytest
from django.contrib.auth.models import User
from django.test import Client

from billing import services as bs
from billing.models import Product
from entries import services as es
from entries.models import CreditEvent, Entry
from ledger import services as ledger
from outreach import services as relay
from taxonomy.services import create_concept

PW = "Correct-horse-battery-9"


def _login(username):
    u = User.objects.create_user(username, f"{username}@example.org", PW)
    c = Client()
    c.force_login(u)
    return u, c


# ---- 1. the person who added an entry cannot prove ownership of it with their own contact ------------------------------------


def test_creator_cannot_claim_by_code_on_a_contact_they_supplied(tree, surgical):
    u, c = _login("selfclaimer")
    e = es.create_entry(
        name="Fake Traders",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=u,
        website="https://fake.example",
        contacts=[("email", "me@mine.example")],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    page = c.post(f"/claim/{e.uid}/", {"action": "send", "channel": "email"}).content.decode()
    assert "cannot prove ownership" in page
    from outreach.models import ClaimOtp

    assert not ClaimOtp.objects.exists()
    # even if the claim object is built directly, the service refuses
    claim = es.start_claim(e, u, "otp_email", "x")
    with pytest.raises(es.EntryError, match="cannot prove ownership"):
        es.approve_claim_by_code(claim, e.contact_set.first())
    e.refresh_from_db()
    assert e.publish_state == "draft" and e.claim_state == "pending"


def test_creator_owner_check_by_a_moderator_never_makes_their_credit_payable(tree, surgical, users):
    creator = users["adder"]
    e = es.create_entry(
        name="Own Shop",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=creator,
        website="https://own.example",
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    claim = es.start_claim(e, creator, "documents", "I run this shop, here is my licence number 12345")
    es.decide_claim(claim, actor=users["mod"], approve=True)  # a moderator reviewed the documents
    e.refresh_from_db()
    assert e.publish_state == "published"  # the owner label is fair: a person reviewed it
    credit = CreditEvent.objects.get(entry=e, kind="added")
    assert credit.eligible is False  # but the person who added it still earns nothing from their own claim


def test_an_independent_surveyor_check_still_makes_the_credit_payable(entry, users):
    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    assert CreditEvent.objects.get(entry=entry, kind="added").eligible is True


def test_someone_else_claiming_by_code_still_works_and_makes_credit_payable(entry, users):
    es.add_contact(entry, "email", "owner@shop.example")
    contact = entry.contact_set.filter(kind="email").first()
    claim = es.start_claim(entry, users["owner"], "otp_email", "code verified")
    es.approve_claim_by_code(claim, contact)
    entry.refresh_from_db()
    assert entry.claim_state == "claimed"
    assert CreditEvent.objects.get(entry=entry, kind="added").eligible is True


# ---- 2. the list type decides whether an entry is a person ------------------------------------------------------------------


def test_form_cannot_list_a_person_as_a_business(tree, db):
    from taxonomy.models import ListTypeSettings

    doctors = create_concept(kind="list_type", name="Private doctors", entity_type_default="person")
    ListTypeSettings.objects.filter(concept=doctors).update(is_individual=True)
    u, c = _login("sneaky")
    r = c.post(
        "/add/",
        {
            "type": doctors.slug,
            "name": "Dr Private",
            "place": tree["paris"].uid,
            "rights": "1",
            "entity_type": "business",
        },
    )
    assert b"not open in this country" in r.content  # the country switch for individuals still applies
    assert not Entry.objects.filter(name="Dr Private").exists()


def test_service_keeps_people_lists_as_people_and_refuses_made_up_types(tree, db, users):
    doctors = create_concept(kind="list_type", name="Tutors", entity_type_default="person")
    e = es.create_entry(
        name="Ms Tutor", place=tree["paris"], primary_concept=doctors, created_by=users["adder"], entity_type="business"
    )
    assert e.entity_type == "person"
    shop = create_concept(kind="list_type", name="Fabric shops")
    assert es.entity_type_for(shop, "nonsense") == "business"
    assert es.entity_type_for(shop, "person") == "person"  # a stricter request is honoured


# ---- 3. a subscription cannot unlock more than the price paid for ------------------------------------------------------------


def test_scope_price_rises_with_place_size_and_with_every_list_type(db, tree, surgical, settings):
    bs.seed_products()
    p = Product.objects.get(key="subscription-city-month")
    buyer = User.objects.create_user("buyer3", "b3@example.org", PW)
    city = bs.create_order(buyer, p, scope_path="pk.punjab.sialkot", concept=surgical)
    country = bs.create_order(buyer, p, scope_path="pk", concept=surgical)
    anytype = bs.create_order(buyer, p, scope_path="pk.punjab.sialkot", concept=None)
    assert city.amount_minor == 2900
    assert country.amount_minor == 2900 * 20 and anytype.amount_minor == 2900 * 3
    with pytest.raises(bs.BillingError, match="whole world"):
        bs.create_order(buyer, p, scope_path="", concept=surgical)
    la = Product.objects.get(key="list-access-30")
    with pytest.raises(bs.BillingError):
        bs.create_order(buyer, la, scope_path="", concept=surgical)
    with pytest.raises(bs.BillingError):
        bs.create_order(buyer, la, scope_path="pk", concept=None)


# ---- 4. payout details cannot be swapped between approval and payment -------------------------------------------------------


def test_payout_details_swapped_after_creation_block_approval_and_payment(db, tree, surgical, users, settings):
    import datetime
    from datetime import timedelta

    from core import clock
    from entries.models import CreditEvent as CE
    from ledger.models import RatePhase

    RatePhase.objects.create(name="P", starts_on=datetime.date(2020, 1, 1), rate_percent=50)
    fin1, fin2 = (User.objects.create_user(n, f"{n}@x.org", "x") for n in ("fin_a", "fin_b"))
    worker = users["adder"]
    es_ = es.create_entry(
        name="Paid Works",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=worker,
        website="https://p.example",
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    es.record_verification(
        es_, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    assert CE.objects.get(entry=es_).eligible
    ledger.record_sale(
        "SW1",
        "list",
        gross=100000,
        scope_path="pk.punjab.sialkot",
        concept=surgical,
        now=clock.now() - timedelta(days=30),
    )
    ledger.release_holds()
    ledger.decide_kyc(
        ledger.submit_kyc(worker, legal_name="W", country_code="PK", method="bank", account="PK11 REAL"),
        actor=fin2,
        approve=True,
    )
    p = ledger.create_payout(worker, creator=fin1, amount_minor=10000)
    assert p.details_hash and p.method == "bank"  # the method comes from the approved profile
    ledger.submit_kyc(worker, legal_name="W", country_code="PK", method="bank", account="PK99 ATTACKER")  # swapped
    with pytest.raises(ledger.LedgerError, match="changed"):
        ledger.approve_payout(p, approver=fin2)
    from ledger.models import PayoutProfile

    ledger.decide_kyc(
        PayoutProfile.objects.get(user=worker), actor=fin2, approve=True
    )  # approved again, but a different account
    with pytest.raises(ledger.LedgerError, match="changed"):
        ledger.approve_payout(p, approver=fin2)
    ledger.cancel_payout(p, actor=fin1, reason="details changed")
    assert ledger.payable_balance(worker) == 50000  # the whole amount is available again
    p2 = ledger.create_payout(worker, creator=fin1, amount_minor=10000)
    ledger.approve_payout(p2, approver=fin2)
    ledger.submit_kyc(worker, legal_name="W", country_code="PK", method="bank", account="PK55 LATE SWAP")
    with pytest.raises(ledger.LedgerError, match="changed"):
        ledger.mark_paid(p2, external_ref="BANK-X")


# ---- 5. reply-to is one clean email address ----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad",
    [
        "a@b.example +92300 000 0000",
        "a@b.example\nBcc: x@y.example",
        "no-at-sign",
        "a@b.example http://phish.example",
        "x" * 300 + "@b.example",
        "",
    ],
)
def test_reply_to_must_be_a_single_clean_email(entry, users, bad):
    with pytest.raises(relay.RelayError):
        relay.send_enquiry(users["adder"], [entry], "Do you make forceps?", bad)


def test_a_clean_reply_to_still_works(entry, users):
    es.add_contact(entry, "email", "shop@example.org")
    from outreach.models import Optin  # noqa: F401

    c = entry.contact_set.get(kind="email")
    relay.record_optin(c, method="claim_otp", wording_version="v1")
    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    enq, counts = relay.send_enquiry(users["owner"], [entry], "Do you make forceps?", "Buyer@Example.org")
    assert counts["delivered"] == 1 and enq.pk
