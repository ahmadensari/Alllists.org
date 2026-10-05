import json
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.test import Client

from billing import services as billing
from billing.models import Product
from core import clock
from core.models import AuditLog, CountrySwitch
from entries import services as es
from entries.models import Contact
from ledger import services as ledger
from outreach import campaigns as cp
from outreach import services as relay
from outreach.models import DeliveryEvent, MessageTemplate, SupplierVerification
from outreach.providers import SandboxProvider

PW = "Correct-horse-battery-9"
NOON_PK = clock.now().replace(hour=7, minute=0, second=0, microsecond=0)  # 12:00 in Karachi
NIGHT_PK = clock.now().replace(hour=22, minute=0, second=0, microsecond=0)  # 03:00 in Karachi


@pytest.fixture(autouse=True)
def rules(settings):
    settings.OUTREACH_SHARE_PERCENT = 10
    settings.MESSAGING_WEBHOOK_SECRETS = {"sandbox": "msg-secret-for-tests"}
    settings.OUTREACH_PAUSE_MIN_SAMPLE = 5


@pytest.fixture
def world(tree, surgical, make_published, users, db):
    CountrySwitch.objects.create(country_code="PK", outreach_on=True, outreach_channels=["whatsapp", "email"])
    entries = []
    for i in range(6):
        e = make_published(f"Shop {i} Works", tree["paris"], phone=f"0300 700 000{i}", refresh=False)
        es.add_contact(e, "whatsapp", f"0300 800 000{i}")
        c = Contact.objects.get(entry=e, kind="whatsapp")
        relay.record_optin(c, method="claim_otp", wording_version="v1")
        entries.append(e)
    buyer = User.objects.create_user("supplier1", "s@x.org", PW)
    sv = cp.request_supplier_verification(buyer, "Acme Steel")
    mod = users["mod"]
    cp.decide_supplier(sv, actor=mod, approve=True)
    tpl = MessageTemplate.objects.create(
        key="intro",
        channel="whatsapp",
        language="en",
        provider_state="approved",
        body="Hello from {company}. We supply {category}. {note}",
    )
    return dict(entries=entries, buyer=buyer, tpl=tpl, mod=mod, **tree, concept=surgical)


def make_campaign(w, **kw):
    args = dict(
        scope_path="pk.punjab.sialkot",
        concept=w["concept"],
        template=w["tpl"],
        channel="whatsapp",
        variables={"company": "Acme Steel", "category": "steel sheets", "note": "Prices on request"},
        budget_minor=100,
    )
    args.update(kw)
    return cp.create_campaign(w["buyer"], **args)


def fund(w, campaign):
    p = Product.objects.get_or_create(
        key="outreach", defaults=dict(name="Outreach campaign", kind="outreach", price_minor=0)
    )[0]
    o = billing.create_order(w["buyer"], p, campaign=campaign)
    billing.record_payment(o, provider="manual", provider_ref=f"OC{campaign.pk}", amount_minor=o.amount_minor)
    campaign.refresh_from_db()
    return o


def test_template_rendering_limits_and_scans_variables(world):
    t = world["tpl"]
    assert cp.render_template(t, {"company": "A", "category": "B", "note": "C"}) == "Hello from A. We supply B. C"
    for bad in ("call 0300 123 4567", "mail me@x.com", "see https://x.example"):
        with pytest.raises(cp.CampaignError):
            cp.render_template(t, {"company": "A", "category": "B", "note": bad})
    with pytest.raises(cp.CampaignError):
        cp.render_template(t, {"company": "x" * 201, "category": "B", "note": "C"})


def test_creation_rules(world, settings):
    w = world
    stranger = User.objects.create_user("stranger", "x@x.org", PW)
    with pytest.raises(cp.CampaignError, match="verified"):
        cp.create_campaign(
            stranger,
            scope_path="pk",
            concept=w["concept"],
            template=w["tpl"],
            channel="whatsapp",
            variables={},
            budget_minor=100,
        )
    with pytest.raises(cp.CampaignError, match="not open"):
        make_campaign(w, scope_path="ae.dubai")
    with pytest.raises(cp.CampaignError, match="approved template"):
        make_campaign(
            w,
            template=MessageTemplate.objects.create(
                key="x", channel="whatsapp", body="Hi {company}", provider_state="draft"
            ),
        )
    with pytest.raises(cp.CampaignError, match="budget"):
        make_campaign(w, budget_minor=10)
    with pytest.raises(cp.CampaignError, match="opted in"):
        make_campaign(
            w,
            scope_path="pk.punjab",
            concept=__import__("taxonomy.services", fromlist=["x"]).create_concept(
                kind="list_type", name="Other trade"
            ),
        )
    settings.OUTREACH_SHARE_PERCENT = None
    with pytest.raises(cp.CampaignError, match="share"):
        make_campaign(w)


def test_off_by_default_per_country_and_channel(world):
    sw = CountrySwitch.objects.get(country_code="PK")
    sw.outreach_channels = ["email"]
    sw.save()
    with pytest.raises(cp.CampaignError, match="not open"):
        make_campaign(world)
    sw.outreach_on, sw.outreach_channels = False, ["whatsapp"]
    sw.save()
    with pytest.raises(cp.CampaignError, match="not open"):
        make_campaign(world)


def test_full_flow_approval_funding_send_report_and_money(world):
    w = world
    c = make_campaign(w, budget_minor=200)
    prov = SandboxProvider()
    with pytest.raises(cp.CampaignError, match="approved"):
        cp.send_batch(c, prov, now=NOON_PK)
    cp.approve_campaign(c, actor=w["mod"])
    with pytest.raises(cp.CampaignError, match="funded"):
        cp.send_batch(c, prov, now=NOON_PK)
    fund(w, c)
    counts = cp.send_batch(c, prov, now=NOON_PK)
    assert counts["sent"] == 6 and len(prov.sent) == 6 and c.spent_minor == 30
    assert all(
        "Hello from Acme Steel" in m["body"] and "/optout/" in m["body"] and m["channel"] == "whatsapp"
        for m in prov.sent
    )
    assert cp.send_batch(c, prov, now=NOON_PK)["sent"] == 0  # nobody is messaged twice
    r = cp.report(c)
    assert r["total"] == 6 and r["replied"] == 0 and r["cost_per_reply_minor"] is None
    # outreach revenue: platform keeps 90 percent, contributors share 10 percent through the ledger
    sale = ledger.Sale.objects.get(order_ref=billing.Order.objects.get(campaign_id=c.pk).ref)
    assert sale.kind == "outreach" and sum(a.amount_minor for a in sale.allocations.all()) == sale.net_minor // 10


def test_quiet_hours_hold_messages_and_caps_hold_the_rest(world, settings):
    w = world
    c = make_campaign(w, budget_minor=200)
    cp.approve_campaign(c, actor=w["mod"])
    fund(w, c)
    prov = SandboxProvider()
    held = cp.send_batch(c, prov, now=NIGHT_PK)
    assert held["held_quiet"] == 6 and not prov.sent
    settings.OUTREACH_DAILY_CAP_PER_SENDER = 4
    counts = cp.send_batch(c, prov, now=NOON_PK)
    assert counts["sent"] == 4 and counts["held_cap"] == 2
    settings.OUTREACH_DAILY_CAP_PER_SENDER, settings.OUTREACH_WEEKLY_CAP_PER_SHOP = 500, 1
    c2 = make_campaign(w, budget_minor=200)  # a second sender run to the same shops
    cp.approve_campaign(c2, actor=w["mod"])
    fund(w, c2)
    assert (
        cp.send_batch(c2, SandboxProvider(), now=NOON_PK + timedelta(days=1))["sent"] == 2
    )  # four shops hit the weekly cap


def test_uae_window_is_shorter(settings):
    d = clock.now().replace(hour=15, minute=0, second=0, microsecond=0)  # 19:00 in Dubai
    assert cp.in_quiet_hours("AE", d) and not cp.in_quiet_hours("PK", d.replace(hour=10))


def callback(provider, secret, payload):
    body = json.dumps(payload).encode()
    return Client().post(
        f"/webhooks/messaging/{provider}/",
        body,
        content_type="application/json",
        HTTP_X_SIGNATURE=cp.sign(secret, body),
    )


def run_sent(w, n=6):
    c = make_campaign(w, budget_minor=200)
    cp.approve_campaign(c, actor=w["mod"])
    fund(w, c)
    cp.send_batch(c, SandboxProvider(), now=NOON_PK)
    return c


def test_callbacks_are_signed_ordered_idempotent_and_drive_the_report(world):
    c = run_sent(world)
    m = c.messages.first()
    assert (
        Client()
        .post("/webhooks/messaging/sandbox/", b"{}", content_type="application/json", HTTP_X_SIGNATURE="bad")
        .status_code
        == 401
    )
    assert Client().post("/webhooks/messaging/none/", b"{}", content_type="application/json").status_code == 404
    for ev in ("delivered", "read"):
        assert (
            callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": ev}).status_code == 200
        )
    assert (
        callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": "read"}).content
        == b"duplicate"
    )
    assert (
        callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": "delivered"}).content
        == b"duplicate"
    )
    callback(
        "sandbox",
        "msg-secret-for-tests",
        {"message_id": m.provider_id, "event": "replied", "reply": "Yes, send a quote"},
    )
    m.refresh_from_db()
    assert (
        m.state == "replied"
        and m.reply_text == "Yes, send a quote"
        and DeliveryEvent.objects.filter(message=m).count() == 3
    )
    assert callback("sandbox", "msg-secret-for-tests", {"message_id": "nope", "event": "read"}).status_code == 400
    assert (
        callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": "weird"}).status_code == 400
    )
    r = cp.report(c)
    assert (
        r["replied"] == 1
        and r["delivered"] == 1
        and r["cost_per_reply_minor"] == 30
        and abs(r["reply_rate"] - 1 / 6) < 1e-9
    )


def test_a_stop_reply_suppresses_the_contact_everywhere(world):
    c = run_sent(world)
    m = c.messages.first()
    callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": "opted_out"})
    m.contact.refresh_from_db()
    assert m.contact.optin_state == "withdrawn" and relay.is_suppressed(m.contact.value_hash)
    assert all(e.pk != m.entry_id for e, _ in cp.recipients("pk.punjab.sialkot", world["concept"], "whatsapp"))


def test_high_opt_out_or_failure_rate_pauses_the_campaign_and_the_sender(world):
    c = run_sent(world)
    msgs = list(c.messages.all())
    callback("sandbox", "msg-secret-for-tests", {"message_id": msgs[0].provider_id, "event": "opted_out"})
    c.refresh_from_db()
    assert c.status == "paused" and "opt-out" in c.pause_reason  # 1 of 6 is over 2 percent
    assert SupplierVerification.objects.get(user=world["buyer"]).state == "paused"
    assert not cp.supplier_verified(world["buyer"])
    with pytest.raises(cp.CampaignError, match="verified"):
        make_campaign(world)


def test_failures_over_ten_percent_also_pause(world):
    c = run_sent(world)
    for m in list(c.messages.all())[:2]:
        callback("sandbox", "msg-secret-for-tests", {"message_id": m.provider_id, "event": "failed"})
    c.refresh_from_db()
    assert c.status == "paused" and "failure" in c.pause_reason


def test_turning_the_country_off_pauses_sending(world):
    c = make_campaign(world, budget_minor=200)
    cp.approve_campaign(c, actor=world["mod"])
    fund(world, c)
    CountrySwitch.objects.filter(country_code="PK").update(outreach_on=False)
    assert cp.send_batch(c, SandboxProvider(), now=NOON_PK) == {"paused": "country switch is off"}
    c.refresh_from_db()
    assert c.status == "paused"


def test_staff_queues_and_buyer_page(world, users):
    from accounts.roles import grant_role

    stranger = User.objects.create_user("newsup", "n@x.org", PW)
    c = Client()
    c.force_login(stranger)
    c.post("/account/campaigns/", {"action": "verify", "company": "New Supplier Ltd"})
    sv = SupplierVerification.objects.get(user=stranger)
    mod = users["mod"]
    grant_role(mod, "moderator")
    mc = Client()
    mc.force_login(mod)
    s = mc.session
    s["mfa_ok"] = True
    s.save()
    assert "New Supplier Ltd" in mc.get("/staff/suppliers/").content.decode()
    mc.post(f"/staff/suppliers/{sv.pk}/approve/")
    sv.refresh_from_db()
    assert sv.state == "verified"
    tpl = MessageTemplate.objects.create(key="t2", channel="email", body="Hi {company}", provider_state="submitted")
    mc.post(f"/staff/templates/{tpl.pk}/approve/")
    tpl.refresh_from_db()
    assert tpl.provider_state == "approved" and tpl.approved_by_id == mod.pk
    camp = make_campaign(world)
    assert (
        str(camp.pk) in mc.get("/staff/campaigns/").content.decode()
        or "supplier1" in mc.get("/staff/campaigns/").content.decode()
    )
    mc.post(f"/staff/campaigns/{camp.pk}/approve/")
    camp.refresh_from_db()
    assert camp.status == "approved"
    page = Client()
    page.force_login(world["buyer"])
    assert "My campaigns" in page.get("/account/campaigns/").content.decode()
    assert AuditLog.objects.filter(action="campaign.approve").exists()
