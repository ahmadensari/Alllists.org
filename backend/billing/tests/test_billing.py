import json

import pytest
from django.contrib.auth.models import User
from django.test import Client

from accounts.roles import grant_role
from billing import services
from billing.models import Invoice, Payment, Product
from core import clock
from entries import services as es
from entries.models import Entry
from ledger.models import Sale

PW = "Correct-horse-battery-9"


@pytest.fixture
def products(db):
    services.seed_products()
    return {p.key: p for p in Product.objects.all()}


@pytest.fixture
def buyer(db):
    return User.objects.create_user("buyerb", "b@x.org", PW)


def test_subscription_order_payment_unlocks_exactly_its_scope_and_records_a_sale(
    products, buyer, tree, surgical, make_published
):
    e = make_published("Crescent Surgical Works", tree["paris"])
    order = services.create_order(
        buyer, products["subscription-city-month"], scope_path="pk.punjab.sialkot", concept=surgical
    )
    c = Client()
    c.force_login(buyer)
    assert "example.org" not in c.get(f"/_f/entry/{e.uid}/").content.decode()
    pay, created = services.record_payment(
        order, provider="manual", provider_ref="BANK-1", amount_minor=order.amount_minor
    )
    assert created
    order.refresh_from_db()
    assert order.state == "fulfilled" and Sale.objects.get(order_ref=order.ref).kind == "subscription"
    assert "https://example.org/crescent" in c.get(f"/_f/entry/{e.uid}/").content.decode()
    assert Invoice.objects.get(order=order).number.startswith("AL-")


def test_payment_is_idempotent_and_must_match_the_amount(products, buyer):
    order = services.create_order(buyer, products["subscription-city-month"], scope_path="pk")
    with pytest.raises(services.BillingError):
        services.record_payment(order, provider="manual", provider_ref="R1", amount_minor=order.amount_minor - 1)
    services.record_payment(order, provider="manual", provider_ref="R2", amount_minor=order.amount_minor)
    again = services.record_payment(order, provider="manual", provider_ref="R2", amount_minor=order.amount_minor)
    assert again[1] is False and Payment.objects.count() == 1 and Sale.objects.count() == 1
    with pytest.raises(services.BillingError):
        services.record_payment(order, provider="manual", provider_ref="R3", amount_minor=order.amount_minor)


def test_refund_revokes_access_and_reverses_the_ledger(products, buyer, tree, surgical, make_published):
    from ledger import services as ledger
    from ledger.models import LedgerAccount

    e = make_published("Crescent Surgical Works", tree["paris"])
    order = services.create_order(buyer, products["list-access-30"], scope_path="pk.punjab.sialkot", concept=surgical)
    services.record_payment(order, provider="manual", provider_ref="B2", amount_minor=order.amount_minor)
    c = Client()
    c.force_login(buyer)
    assert "https://example.org/crescent" in c.get(f"/_f/entry/{e.uid}/").content.decode()
    services.refund_order(order, actor=buyer)
    assert "https://example.org/crescent" not in c.get(f"/_f/entry/{e.uid}/").content.decode()
    assert all(ledger.balance(a) == 0 for a in LedgerAccount.objects.all())
    order.refresh_from_db()
    assert order.state == "refunded"
    with pytest.raises(services.BillingError):
        services.refund_order(order, actor=buyer)


def test_tax_is_added_from_country_configuration(products, buyer, settings, tree, surgical):
    settings.TAX_RATES = {"PK": "17"}
    order = services.create_order(
        buyer, products["subscription-city-month"], scope_path="pk.punjab.sialkot", concept=surgical
    )
    assert order.tax_minor == 493 and order.amount_minor == 2900 + 493
    services.record_payment(
        order, provider="manual", provider_ref="T1", amount_minor=order.amount_minor, fees_minor=100
    )
    sale = Sale.objects.get(order_ref=order.ref)
    assert sale.tax_minor == 493 and sale.net_minor == order.amount_minor - 493 - 100
    assert [line["item"] for line in Invoice.objects.get(order=order).lines] == [
        products["subscription-city-month"].name,
        "Tax 17%",
    ]


def signed_post(provider, secret, payload):
    body = json.dumps(payload).encode()
    return Client().post(
        f"/webhooks/payments/{provider}/",
        body,
        content_type="application/json",
        HTTP_X_SIGNATURE=services.sign(secret, body),
    )


def test_webhook_signature_and_replay_are_safe(products, buyer, settings):
    settings.PAYMENT_WEBHOOK_SECRETS = {"gateway": "s3cret-for-tests"}
    order = services.create_order(buyer, products["subscription-city-month"], scope_path="pk")
    payload = {"event_id": "evt-1", "order_ref": order.ref, "status": "succeeded", "amount_minor": order.amount_minor}
    bad = Client().post(
        "/webhooks/payments/gateway/",
        json.dumps(payload).encode(),
        content_type="application/json",
        HTTP_X_SIGNATURE="deadbeef",
    )
    assert bad.status_code == 401 and Payment.objects.count() == 0
    assert Client().post("/webhooks/payments/nobody/", b"{}", content_type="application/json").status_code == 404
    r1 = signed_post("gateway", "s3cret-for-tests", payload)
    r2 = signed_post("gateway", "s3cret-for-tests", payload)
    assert r1.content == b"recorded" and r2.content == b"duplicate"
    assert Payment.objects.count() == 1 and Sale.objects.count() == 1
    wrong = dict(payload, event_id="evt-2", amount_minor=1)
    assert signed_post("gateway", "s3cret-for-tests", wrong).status_code == 409
    assert signed_post("gateway", "s3cret-for-tests", {"order_ref": "x"}).status_code == 400


def test_company_page_purchase_activates_the_plan_and_the_moderated_text_shows(
    products, tree, surgical, users, make_published, db
):
    e = make_published("Crescent Surgical Works", tree["paris"])
    owner = users["owner"]
    claim = es.start_claim(e, owner, "documents", "I run it")
    es.decide_claim(claim, actor=users["mod"], approve=True)
    order = services.create_order(owner, products["company-page-quarter"], entry=e)
    with pytest.raises(es.GuardError):
        es.save_company_section(e, owner, "about", "We make surgical scissors since 1980.")
    services.record_payment(order, provider="manual", provider_ref="CP1", amount_minor=order.amount_minor)
    e.refresh_from_db()
    assert e.listing_plan == "company" and e.plan_valid_until >= clock.today()
    c = Client()
    c.force_login(owner)
    assert "Add certificate" in c.get(f"/account/owner/{e.uid}/").content.decode()
    c.post(
        f"/account/owner/{e.uid}/",
        {"action": "section", "kind": "about", "body": "We make surgical scissors since 1980."},
    )
    c.post(f"/account/owner/{e.uid}/", {"action": "certificate", "scheme": "ISO 13485", "value": "CERT-77"})
    html = Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "since 1980" not in html  # waits for a moderator
    section = e.company_sections.get()
    es.moderate_company_section(section, actor=users["mod"], approve=True)
    html = Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "since 1980" in html and "Provided by the company" in html and "Company says" in html and "CERT-77" in html
    es.record_verification(
        e,
        field_group="certificates",
        level="surveyor",
        actor=users["surveyor"],
        method="visit",
        evidence="Saw the certificate",
    )
    assert "Checked by AllLists" in Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "Company page" in Client().get("/pk/punjab/sialkot/surgical-instrument-makers/").content.decode()


def test_links_are_not_allowed_in_company_text_and_expired_plans_hide_sections(
    products, tree, users, make_published, db
):
    e = make_published("Crescent Surgical Works", tree["paris"])
    owner = users["owner"]
    es.decide_claim(es.start_claim(e, owner, "documents", "me"), actor=users["mod"], approve=True)
    es.activate_company_plan(e, days=30)
    with pytest.raises(es.EntryError):
        es.save_company_section(e, owner, "about", "Visit https://spam.example now")
    s = es.save_company_section(e, owner, "about", "We are a family firm.")
    es.moderate_company_section(s, actor=users["mod"], approve=True)
    assert "family firm" in Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    Entry.objects.filter(pk=e.pk).update(plan_valid_until=clock.today().replace(year=clock.today().year - 1))
    html = Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "family firm" not in html and "Is this your business" in html


def test_people_and_child_services_cannot_buy_company_pages(
    products, tree, surgical, users, make_published, pk_open, db
):
    p = es.create_entry(
        name="Dr Solo",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        entity_type="person",
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    with pytest.raises(es.EntryError):
        es.activate_company_plan(p, days=30)


def test_only_the_owner_can_order_a_company_page(products, buyer, tree, make_published):
    e = make_published("Crescent Surgical Works", tree["paris"])
    with pytest.raises(services.BillingError):
        services.create_order(buyer, products["company-page-quarter"], entry=e)


def test_staff_record_payment_screen_needs_finance_role(products, buyer, db):
    order = services.create_order(buyer, products["subscription-city-month"], scope_path="pk")
    fin = User.objects.create_user("finx", "f@x.org", PW)
    grant_role(fin, "finance")
    c = Client()
    c.force_login(fin)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    assert order.ref in c.get("/staff/orders/").content.decode()
    c.post("/staff/orders/", {"order": order.ref, "amount_minor": order.amount_minor, "reference": "BANK-77"})
    order.refresh_from_db()
    assert order.state == "fulfilled"
    plain = Client()
    plain.force_login(buyer)
    assert plain.get("/staff/orders/").status_code == 403


def test_buyer_pages(products, buyer, tree, surgical):
    c = Client()
    assert c.get("/account/subscription/")["Location"].startswith("/account/login/")
    c.force_login(buyer)
    refused = c.post("/account/subscription/", {"product": "subscription-city-month", "scope": ""})
    assert refused.status_code == 200 and b"whole world" in refused.content  # no world-wide access at the city price
    r = c.post(
        "/account/subscription/",
        {"product": "subscription-city-month", "scope": "pk.punjab.sialkot", "type": surgical.slug},
    )
    ref = r["Location"].rstrip("/").split("/")[-1]
    page = c.get(f"/account/orders/{ref}/").content.decode()
    assert ref in page and "pending" in page
    other = Client()
    other.force_login(User.objects.create_user("nosy", "n@x.org", PW))
    assert other.get(f"/account/orders/{ref}/").status_code == 404
