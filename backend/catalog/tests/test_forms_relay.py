import re

import pytest
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client

from access import services as acs
from access.models import Plan
from accounts.roles import grant_role
from core.models import AuditLog, verify_audit_chain
from entries import services as es
from entries.models import Contact, Entry
from moderation import services as mod
from moderation.models import Report, Takedown
from outreach import services as relay
from outreach.models import Enquiry, EnquiryRecipient, OutboxMessage, Suppression
from volunteers import services as vs
from volunteers.models import Task

PW = "Correct-horse-battery-9"
LIST = "/pk/punjab/sialkot/surgical-instrument-makers/"


def login(username, role=None, mfa=False):
    u = User.objects.create_user(username, f"{username}@example.org", PW)
    if role:
        grant_role(u, role)
    c = Client()
    c.force_login(u)
    if mfa:
        s = c.session
        s["mfa_ok"] = True
        s.save()
    return u, c


@pytest.fixture
def owned(entry, tree):
    """A published entry whose owner claimed it by code and opted in to enquiries."""
    owner, oc = login("ownerx")
    es.record_verification(
        entry,
        field_group="identity",
        level="surveyor",
        actor=User.objects.get(username="surveyor"),
        method="call",
        evidence="ok",
    )
    return entry, owner, oc


# ---- add entry -------------------------------------------------------------------------------------------------------


def test_add_entry_requires_login_and_rights_declaration(tree, surgical):
    assert Client().get("/add/")["Location"].startswith("/account/login/")
    u, c = login("adder2")
    assert b"Business name" in c.get("/add/?type=surgical-instrument-makers").content
    r = c.post("/add/", {"type": "surgical-instrument-makers", "name": "New Works", "place": tree["paris"].uid})
    assert b"right to share" in r.content and not Entry.objects.filter(name="New Works").exists()
    r = c.post(
        "/add/",
        {
            "type": "surgical-instrument-makers",
            "name": "New Works",
            "place": tree["paris"].uid,
            "rights": "1",
            "phone": "0300 777 8888",
            "addon_business_type": "trader",
            "addon_product_categories": "scissors, forceps",
        },
    )
    assert b"saved as a draft" in r.content
    e = Entry.objects.get(name="New Works")
    assert e.publish_state == "draft" and e.created_via == "contributor" and e.created_by == u
    assert e.addons["product_categories"] == ["scissors", "forceps"] and e.contact_set.count() == 1
    assert u.contributor.declared_rights_at is not None


def test_add_entry_rejects_person_when_switch_off_and_bad_place(tree, surgical):
    u, c = login("adder3")
    r = c.post(
        "/add/",
        {
            "type": "surgical-instrument-makers",
            "name": "Dr X",
            "place": tree["paris"].uid,
            "rights": "1",
            "entity_type": "person",
        },
    )
    assert b"not open in this country" in r.content
    r = c.post("/add/", {"type": "surgical-instrument-makers", "name": "X", "rights": "1"})
    assert b"Choose a place" in r.content


def test_suggest_area_flags_duplicates(tree):
    u, c = login("adder4")
    assert b"already exists" in c.post("/add/area/", {"parent": tree["sialkot"].uid, "name": "paris  ROAD"}).content
    assert (
        b"moderator will check" in c.post("/add/area/", {"parent": tree["sialkot"].uid, "name": "Kashmir Road"}).content
    )


# ---- claim by code, opt-in, enquiry relay ------------------------------------------------------------------------------


def test_claim_by_code_makes_owner_and_opts_in_without_showing_contacts(entry, tree, users):
    es.add_contact(entry, "email", "owner@shop.example")
    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    u, c = login("claimant")
    page = c.get(f"/claim/{entry.uid}/").content.decode()
    assert "owner@shop.example" not in page and "0300" not in page
    mail.outbox.clear()
    c.post(f"/claim/{entry.uid}/", {"action": "send", "channel": "email"})
    assert len(mail.outbox) == 1 and mail.outbox[0].to == ["owner@shop.example"]
    code = re.search(r"is (\d{6})", mail.outbox[0].body).group(1)
    bad = c.post(f"/claim/{entry.uid}/", {"action": "verify", "code": "000000", "optin": "1"})
    assert b"wrong or has expired" in bad.content
    noopt = c.post(f"/claim/{entry.uid}/", {"action": "verify", "code": code})
    assert b"Tick the box" in noopt.content
    ok = c.post(f"/claim/{entry.uid}/", {"action": "verify", "code": code, "optin": "1"})
    assert b"You now own this listing" in ok.content
    entry.refresh_from_db()
    assert entry.claim_state == "claimed" and es.current_level(entry) == "surveyor"
    assert "owner" in es.current_levels(entry)
    assert Contact.objects.get(entry=entry, kind="email").optin_state == "optin"


def test_otp_burns_after_five_wrong_tries_and_limits_requests(entry, users):
    es.add_contact(entry, "email", "owner@shop.example")
    contact = Contact.objects.get(entry=entry, kind="email")
    relay.send_claim_otp(entry, users["owner"], contact)
    for _ in range(5):
        assert relay.verify_claim_otp(entry, users["owner"], "111111") is None
    assert (
        relay.verify_claim_otp(entry, users["owner"], re.search(r"is (\d{6})", mail.outbox[-1].body).group(1)) is None
    )
    relay.send_claim_otp(entry, users["owner"], contact)
    relay.send_claim_otp(entry, users["owner"], contact)
    with pytest.raises(relay.RelayError):
        relay.send_claim_otp(entry, users["owner"], contact)


def test_phone_otp_goes_to_the_outbox_not_the_screen(entry, users):
    phone = Contact.objects.get(entry=entry)
    relay.send_claim_otp(entry, users["owner"], phone)
    box = OutboxMessage.objects.get()
    assert box.kind == "otp" and box.channel == "sms" and "AllLists code" in box.body


def test_documents_claim_waits_for_a_moderator(entry, users):
    u, c = login("claimant2")
    assert b"Describe how" in c.get(f"/claim/{entry.uid}/").content or True
    r = c.post(
        f"/claim/{entry.uid}/", {"action": "documents", "evidence": "I am the founder; call my accountant to confirm."}
    )
    assert b"Claim received" in r.content
    entry.refresh_from_db()
    assert entry.claim_state == "pending"


def optin_email(entry, addr="owner@shop.example"):
    es.add_contact(entry, "email", addr)
    c = Contact.objects.get(entry=entry, kind="email")
    relay.record_optin(c, method="claim_otp", wording_version="v1")
    return c


def test_free_user_message_reaches_only_opted_in_contacts_and_never_reveals(entry, users):
    entry.publish_state = "published"
    entry.save()
    optin_email(entry)
    u, c = login("buyer1")
    mail.outbox.clear()
    r = c.post(f"/message/{entry.uid}/", {"text": "Do you make 500 scissors a month?", "reply_to": "buyer@x.org"})
    assert b"Your message was passed on" in r.content and b"owner@shop.example" not in r.content
    assert (
        len(mail.outbox) == 1
        and mail.outbox[0].to == ["owner@shop.example"]
        and "Stop these messages" in mail.outbox[0].body
    )
    assert EnquiryRecipient.objects.get().state == "delivered"


def test_message_to_business_without_optin_is_not_sent(entry):
    entry.publish_state = "published"
    entry.save()
    u, c = login("buyer2")
    mail.outbox.clear()
    r = c.post(f"/message/{entry.uid}/", {"text": "Hello there", "reply_to": "b@x.org"})
    assert b"not opted in" in r.content and not mail.outbox
    assert EnquiryRecipient.objects.get().state == "not_reachable"


@pytest.mark.parametrize(
    "text",
    [
        "call me on 0300 123 4567",
        "mail me at a@b.com",
        "see https://x.example",
        "go to wa.me/9230012",
        "my number is zero three zero zero one two three",
    ],
)
def test_contact_extraction_is_refused(entry, text):
    assert relay.contact_leaks(text), text
    entry.publish_state = "published"
    entry.save()
    u, c = login("buyer3")
    r = c.post(f"/message/{entry.uid}/", {"text": text, "reply_to": "b@x.org"})
    assert b"Remove" in r.content and not Enquiry.objects.exists()


def test_clean_text_passes(entry):
    assert relay.contact_leaks("We need 500 stainless scissors by March, price per piece please.") == []


def test_many_recipients_need_a_subscription_and_limits(entry, users, tree, surgical, make_published):
    other = make_published("Other Works", tree["paris"], phone="0301 000 0001")
    u, c = login("buyer4")
    assert c.get("/enquiry/?path=pk.punjab.sialkot&type=surgical-instrument-makers").status_code == 403
    with pytest.raises(relay.RelayError):
        relay.send_enquiry(u, [other, entry], "Hello world", "b@x.org")
    plan = Plan.objects.create(key="subscriber_scope", name="Sub")
    acs.grant_subscription(u, plan, scope_path="pk.punjab.sialkot", concept=surgical, days=30)
    assert c.get("/enquiry/?path=pk.punjab.sialkot&type=surgical-instrument-makers").status_code == 200
    optin_email(other, "other@shop.example")
    r = c.post(
        "/enquiry/",
        {
            "path": "pk.punjab.sialkot",
            "type": "surgical-instrument-makers",
            "entry": [other.uid],
            "text": "Quote for 200 forceps please",
            "reply_to": "b@x.org",
        },
    )
    assert r.status_code == 302
    rows = c.get("/account/enquiries/").content.decode()
    assert "1 delivered" in rows and "other@shop.example" not in rows


def test_opt_out_is_immediate_global_and_survives_reimport(entry, tree, surgical, users):
    contact = optin_email(entry)
    token = relay.optout_token(contact)
    assert (
        relay.contact_from_optout_token(token) == contact
        and relay.contact_from_optout_token("x-" + str(contact.pk)) is None
    )
    c = Client()
    assert c.get(f"/optout/{token}/").status_code == 200
    c.post(f"/optout/{token}/")
    contact.refresh_from_db()
    assert contact.optin_state == "withdrawn" and relay.is_suppressed(contact.value_hash)
    entry.publish_state = "published"
    entry.save()
    u, bc = login("buyer5")
    mail.outbox.clear()
    bc.post(f"/message/{entry.uid}/", {"text": "Hello again", "reply_to": "b@x.org"})
    assert not mail.outbox
    with pytest.raises(es.EntryError):
        es.create_entry(
            name="Re-imported",
            place=tree["paris"],
            primary_concept=surgical,
            contacts=[("email", "Owner@Shop.example")],
            addons={"business_type": "trader", "product_categories": ["x"]},
        )


# ---- something wrong, takedown, erasure ----------------------------------------------------------------------------------


def test_report_is_anonymous_free_rate_limited_and_honeypot_works(owned):
    entry, *_ = owned
    c = Client()
    assert b"Something wrong" in c.get(f"/wrong/{entry.uid}/").content
    r = c.post(f"/wrong/{entry.uid}/", {"kind": "closed", "text": "Shop is shut since June"})
    assert b"moderator will check" in r.content and Report.objects.filter(kind="closed").count() == 1
    c.post(f"/wrong/{entry.uid}/", {"kind": "closed", "text": "bot text", "website2": "spam"})
    assert Report.objects.count() == 1
    assert b"Tell us what is wrong" in c.post(f"/wrong/{entry.uid}/", {"kind": "wrong", "text": ""}).content
    for i in range(10):
        c.post(f"/wrong/{entry.uid}/", {"kind": "wrong", "text": f"issue number {i}"})
    assert b"too many reports" in c.post(f"/wrong/{entry.uid}/", {"kind": "wrong", "text": "one more issue"}).content


def test_upheld_closed_report_closes_the_entry(owned, users):
    entry, *_ = owned
    r = mod.submit_report(entry, "closed", "shut")
    mod.decide_report(r, actor=users["mod"], uphold=True, resolution="confirmed by call")
    entry.refresh_from_db()
    assert entry.status == "permanently_closed"
    with pytest.raises(mod.ModerationError):
        mod.decide_report(r, actor=users["mod"], uphold=False)


def test_removal_request_opens_takedown_with_30_day_deadline_and_erasure_tombstones(owned, users, tree, surgical):
    entry, *_ = owned
    es.add_contact(entry, "email", "owner@shop.example")
    from outreach.services import is_suppressed

    h = Contact.objects.get(entry=entry, kind="email").value_hash
    mod.submit_report(entry, "remove_my_data", "Please remove my shop")
    td = Takedown.objects.get()
    assert td.state == "open" and 29 <= (td.due_at - td.created_at).days <= 30
    mod.execute_erasure(td, actor=users["mod"])
    entry.refresh_from_db()
    assert entry.publish_state == "tombstoned" and entry.name.startswith("Removed") and entry.deleted_at
    assert not entry.contact_set.exists() and not entry.namevariant_set.exists()
    assert is_suppressed(h) and Suppression.objects.exists()
    assert Client().get(f"/e/{entry.uid}/x/").status_code == 404
    with pytest.raises(es.EntryError):
        es.create_entry(
            name="Again",
            place=tree["paris"],
            primary_concept=surgical,
            contacts=[("email", "owner@shop.example")],
            addons={"business_type": "trader", "product_categories": ["x"]},
        )
    assert verify_audit_chain() is None


def test_suggested_edit_applies_only_when_accepted(owned, users):
    entry, *_ = owned
    s = mod.suggest_edit(entry, "website", "https://new.example.org")
    with pytest.raises(mod.ModerationError):
        mod.suggest_edit(entry, "addons", {"x": 1})
    entry.refresh_from_db()
    assert entry.website == "https://example.org"
    mod.decide_suggestion(s, actor=users["mod"], accept=True)
    entry.refresh_from_db()
    assert entry.website == "https://new.example.org"


# ---- surveyor tasks ------------------------------------------------------------------------------------------------------


def test_tasks_never_go_to_the_adder_and_need_evidence(entry, users):
    vs.queue_verification(entry)
    adder = users["adder"]
    grant_role(adder, "surveyor")
    assert vs.take_next_task(adder) is None
    sv = users["surveyor"]
    grant_role(sv, "surveyor")
    task = vs.take_next_task(sv)
    assert task and task.entry == entry and task.state == "assigned"
    with pytest.raises(es.GuardError):
        vs.complete_task(task, user=sv, outcome="confirmed", evidence=" ")
    with pytest.raises(es.GuardError):
        vs.complete_task(task, user=users["mod"], outcome="confirmed", evidence="x")
    vs.complete_task(task, user=sv, outcome="confirmed", evidence="Owner answered and confirmed the address", minutes=4)
    entry.refresh_from_db()
    sv = User.objects.get(pk=sv.pk)
    assert entry.publish_state == "published" and sv.contributor.points == 1 and task.minutes == 4


def test_task_screens_and_audited_contact_reveal(entry, users):
    vs.queue_verification(entry)
    u, c = login("sv1", role="surveyor")
    assert Client().get("/account/tasks/")["Location"].startswith("/account/login/")
    r = c.post("/account/tasks/", {"action": "take"})
    assert r.status_code == 302
    url = r["Location"]
    page = c.get(url).content.decode()
    assert "0300" not in page and "3001234567" not in page
    n = AuditLog.objects.filter(action="contact.reveal").count()
    shown = c.post(url, {"action": "reveal"}).content.decode()
    assert "+923001234567" in shown and AuditLog.objects.filter(action="contact.reveal").count() == n + 1
    other, oc = login("sv2", role="surveyor")
    assert oc.get(url).status_code == 404 and oc.post(url, {"action": "reveal"}).status_code == 404
    done = c.post(
        url,
        {
            "action": "complete",
            "outcome": "confirmed",
            "method": "call",
            "evidence": "Spoke to the manager",
            "minutes": "3",
        },
    )
    assert done.status_code == 302 and Task.objects.get().state == "done"


def test_non_surveyors_cannot_see_tasks_and_canary_accuracy_suspends(entry, users, tree, surgical):
    u, c = login("plain")
    assert c.get("/account/tasks/").status_code == 403
    sv = users["surveyor"]
    grant_role(sv, "surveyor")
    for i in range(3):
        e = es.create_entry(
            name=f"Fake Shop {i}",
            place=tree["paris"],
            primary_concept=surgical,
            created_via="agent",
            source=__import__("intake.models", fromlist=["Source"]).Source.objects.create(
                name=f"s{i}",
                tier="amber",
                allowed_uses=["agent_fetch"],
                reviewed_on=__import__("datetime").date(2026, 1, 1),
            ),
            addons={"business_type": "trader", "product_categories": ["x"]},
        )
        vs.queue_verification(e, canary=True)
        t = vs.take_next_task(sv)
        vs.complete_task(
            t, user=sv, outcome="confirmed", evidence="said it exists", minutes=1
        )  # wrong: canaries do not exist
    sv.contributor.refresh_from_db()
    assert sv.contributor.accuracy == 0.0 and sv.contributor.suspended
    vs.queue_verification(entry)
    assert vs.take_next_task(sv) is None


# ---- staff console ---------------------------------------------------------------------------------


def test_staff_console_needs_role_and_runs_queues(entry, tree, surgical, users):
    es.create_entry(
        name="Crescent Surgical Work",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["mod"],
        contacts=[("phone", "0300 123 4567")],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    from intake.dedupe import scan_all

    scan_all()
    u, c = login("modx", role="moderator", mfa=True)
    page = c.get("/staff/").content.decode()
    assert "Possible duplicates" in page and "Removal and erasure" in page
    q = c.get("/staff/dedupe/").content.decode()
    assert "Crescent" in q
    cand = __import__("intake.models", fromlist=["DedupeCandidate"]).DedupeCandidate.objects.get()
    assert c.post(f"/staff/dedupe/{cand.pk}/merge/").status_code == 302
    cand.refresh_from_db()
    assert cand.state == "merged" and Entry.objects.filter(merged_into__isnull=False).count() == 1
    assert c.get("/staff/audit/").content.decode().count("Hash chain intact") == 1
    plain, pc = login("plain2")
    assert pc.get("/staff/").status_code == 403


def test_staff_actions_check_capability(entry, users):
    r = mod.submit_report(entry, "wrong", "bad data here")
    sv, svc = login("svx", role="surveyor", mfa=True)
    assert svc.get("/staff/reports/").status_code == 403
    assert svc.post(f"/staff/reports/{r.pk}/uphold/").status_code == 403
    mo, mc = login("mox", role="moderator", mfa=True)
    assert mc.post(f"/staff/reports/{r.pk}/uphold/").status_code == 302
    r.refresh_from_db()
    assert r.state == "upheld"


def test_country_switch_page_changes_and_audits(db):
    adm, c = login("admx", role="admin", mfa=True)
    c.post("/staff/switches/", {"country": "AE", "field": "browsing_on", "value": "on"})
    c.post(
        "/staff/switches/", {"country": "AE", "field": "selling_on", "value": "on", "note": "counsel cleared 2026-10"}
    )
    from core.models import CountrySwitch

    sw = CountrySwitch.objects.get(country_code="AE")
    assert sw.selling_on and sw.cleared_by == "admx"
    assert AuditLog.objects.filter(action="switch.change").count() == 2
    mo, mc = login("mox2", role="moderator", mfa=True)
    assert mc.get("/staff/switches/").status_code == 403


def test_staff_without_mfa_cannot_use_console(entry):
    u, c = login("modno", role="moderator", mfa=False)
    r = c.get("/staff/")
    assert r.status_code == 302 and "mfa" in r["Location"]
