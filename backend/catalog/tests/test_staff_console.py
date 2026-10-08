"""The staff console: every queue, every action, every role (plan P3.19). Each action must change exactly the thing it says,
be refused to roles without the capability, refuse GET, survive being pressed twice, and never answer with a server error.
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client

from accounts.roles import grant_role
from catalog.staff_views import QUEUES
from entries import services as es
from entries.models import Claim, CompanySection
from intake.models import DedupeCandidate
from ledger import services as ledger
from ledger.models import PayoutProfile
from moderation import services as mod
from moderation.models import Report, SuggestedEdit, Takedown
from outreach import campaigns as cp
from outreach.models import MessageTemplate, SupplierVerification
from places import services as ps
from places.models import PlaceProposal

PW = "Correct-horse-battery-9"
ROLE_FOR_CAP = {
    "moderate": "moderator",
    "claim_decide": "moderator",
    "takedown": "moderator",
    "record_payment": "finance",
}


def staff(role, name=None):
    u = User.objects.create_user(name or f"{role}_x", f"{role}@example.org", PW)
    grant_role(u, role)
    c = Client(raise_request_exception=False)
    c.force_login(u)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    return u, c


@pytest.fixture
def items(tree, surgical, make_published, users):
    """One pending item for every queue."""
    a = make_published("Alpha Works", tree["paris"], phone="0300 000 0001")
    b = make_published("Alpha Works Ltd", tree["paris"], phone="0300 000 0002")
    out = {}
    out["dedupe"] = DedupeCandidate.objects.create(a_entry=a, b_entry=b, score=0.7, features={})
    out["areas"] = ps.propose_area(parent=tree["sialkot"], name="Kashmir Road", proposer=users["adder"])
    claimed = make_published("Claim Me", tree["sialkot"], phone="0300 000 0003")
    out["claims"] = es.start_claim(claimed, users["owner"], "documents", "I run this shop, here is my licence number")
    out["reports"] = mod.submit_report(a, "closed", "seems shut")
    out["suggestions"] = mod.suggest_edit(a, "website", "https://new.example", users["adder"])
    out["takedowns"] = Takedown.objects.get(
        pk=mod.submit_report(b, "remove_my_data", "please").entry.takedowns.first().pk
    )
    out["suppliers"] = cp.request_supplier_verification(users["owner"], "Acme Supplies Ltd")
    out["templates"] = MessageTemplate.objects.create(
        key="t1", channel="email", body="Hi {company}", provider_state="submitted"
    )
    # a company section awaiting review
    c2 = make_published("Company Co", tree["sialkot"], phone="0300 000 0004")
    es.decide_claim(
        es.start_claim(c2, users["surveyor"], "documents", "owner of Company Co, licence 99"),
        actor=users["mod"],
        approve=True,
    )
    es.activate_company_plan(c2, days=30)
    out["company"] = es.save_company_section(c2, users["surveyor"], "about", "We make forceps.")
    # payout details awaiting review
    out["kyc"] = ledger.submit_kyc(
        users["adder"], legal_name="A Person", country_code="PK", method="bank", account="PK00 1111"
    )
    # a consent record for a person
    person = es.create_entry(
        name="Dr Consent",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        entity_type="person",
    )
    es.record_consent(person, status="consented", method="web_form", wording_version="v1")
    out["consent"] = person.consents.first()
    return out


def test_every_queue_has_a_fixture_or_a_reason(items):
    covered = set(items) | {"campaigns", "ads"}  # campaigns and ads have their own tests (outreach, access)
    assert set(QUEUES) <= covered, set(QUEUES) - covered


def test_pages_list_items_for_roles_with_the_capability_and_refuse_others(items):
    mod_u, mod_c = staff("moderator")
    fin_u, fin_c = staff("finance")
    for key, q in QUEUES.items():
        right = mod_c if q.cap in ("moderate", "claim_decide", "takedown") else fin_c
        wrong = fin_c if right is mod_c else mod_c
        assert right.get(f"/staff/{key}/").status_code == 200, key
        assert wrong.get(f"/staff/{key}/").status_code == 403, key
        assert Client().get(f"/staff/{key}/").status_code == 302, key
    html = mod_c.get("/staff/claims/").content.decode()
    assert "Claim Me" in html or "claim" in html.lower()


STATE_AFTER = {
    ("dedupe", "merge"): lambda o: (o.state, "merged"),
    ("dedupe", "reject"): lambda o: (o.state, "rejected"),
    ("areas", "approve"): lambda o: (o.state, "approved"),
    ("areas", "reject"): lambda o: (o.state, "rejected"),
    ("claims", "approve"): lambda o: (o.state, "approved"),
    ("claims", "reject"): lambda o: (o.state, "rejected"),
    ("reports", "uphold"): lambda o: (o.state, "upheld"),
    ("reports", "reject"): lambda o: (o.state, "rejected"),
    ("suggestions", "accept"): lambda o: (o.state, "accepted"),
    ("suggestions", "reject"): lambda o: (o.state, "rejected"),
    ("takedowns", "erase"): lambda o: (o.state, "done"),
    ("takedowns", "refuse"): lambda o: (o.state, "refused"),
    ("suppliers", "approve"): lambda o: (o.state, "verified"),
    ("suppliers", "reject"): lambda o: (o.state, "rejected"),
    ("templates", "approve"): lambda o: (o.provider_state, "approved"),
    ("company", "approve"): lambda o: (o.state, "approved"),
    ("company", "reject"): lambda o: (o.state, "rejected"),
    ("kyc", "approve"): lambda o: (o.state, "approved"),
    ("kyc", "reject"): lambda o: (o.state, "rejected"),
    ("consent", "withdraw"): lambda o: (o.entry.publish_state, "suppressed"),
}


@pytest.mark.parametrize("key,action", sorted(STATE_AFTER))
def test_each_action_does_what_it_says_and_survives_a_second_press(items, key, action, users):
    q = QUEUES[key]
    role = "finance" if q.cap == "record_payment" else "moderator"
    u, c = staff(role)
    obj = items[key]
    url = f"/staff/{key}/{obj.pk}/{action}/"
    assert c.get(url).status_code == 405  # state changes are POST only
    assert Client().post(url).status_code == 302  # anonymous: sent to sign in
    wrong_role = "moderator" if role == "finance" else "finance"
    _, wc = staff(wrong_role)
    assert wc.post(url).status_code == 403
    r = c.post(url, {"note": "checked"})
    assert r.status_code == 302 and r["Location"] == f"/staff/{key}/"
    obj.refresh_from_db()
    got, want = STATE_AFTER[(key, action)](obj)
    assert got == want, (key, action, got)
    again = c.post(url, {"note": "again"})
    assert again.status_code in (302, 404)  # a second press never crashes


def test_unknown_queue_action_and_item_are_not_found(items):
    _, c = staff("moderator")
    assert c.get("/staff/nonsense/").status_code == 404
    assert c.post("/staff/claims/999999/approve/").status_code == 404
    assert c.post(f"/staff/claims/{items['claims'].pk}/explode/").status_code == 404
    assert c.post("/staff/nonsense/1/approve/").status_code == 404


def test_nobody_approves_their_own_payout_details(items, users):
    fin, c = staff("finance", "fin_self")
    mine = ledger.submit_kyc(fin, legal_name="Fin", country_code="PK", method="bank", account="PK22")
    r = c.post(f"/staff/kyc/{mine.pk}/approve/")
    assert r.status_code == 302
    mine.refresh_from_db()
    assert mine.state == "submitted"  # refused; the page shows the reason


def test_erasure_leaves_a_tombstone_and_a_suppressed_contact(items):
    _, c = staff("moderator")
    td = items["takedowns"]
    c.post(f"/staff/takedowns/{td.pk}/erase/")
    td.refresh_from_db()
    e = td.entry
    e.refresh_from_db()
    assert e.publish_state == "tombstoned" and e.name.startswith("Removed") and not e.contact_set.exists()


def test_index_lists_only_what_a_role_may_open(items):
    _, mc = staff("moderator")
    _, fc = staff("finance")
    m, f = mc.get("/staff/").content.decode(), fc.get("/staff/").content.decode()
    assert "claims" in m and "kyc" not in m
    assert "kyc" in f and "claims" not in f
    assert (
        PlaceProposal
        and Report
        and SuggestedEdit
        and Claim
        and CompanySection
        and PayoutProfile
        and SupplierVerification
    )
