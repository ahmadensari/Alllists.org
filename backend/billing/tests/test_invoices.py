import pytest
from django.contrib.auth.models import User
from django.test import Client

from accounts.roles import grant_role
from billing import reporting, services as bs
from billing.models import Invoice, Product

PW = "Correct-horse-battery-9"


@pytest.fixture
def buyer(db):
    bs.seed_products()
    return User.objects.create_user("inv_buyer", "ib@x.org", PW)


def _order(buyer, tree, surgical, key="subscription-city-month", billing=None):
    return bs.create_order(
        buyer, Product.objects.get(key=key), scope_path="pk.punjab.sialkot", concept=surgical, billing=billing
    )


def test_invoices_are_numbered_without_gaps_and_keep_the_tax_rate_of_the_order(buyer, tree, surgical, settings):
    settings.TAX_RATES = {"PK": "16"}
    o1 = _order(buyer, tree, surgical, billing={"name": "Acme Ltd", "tax_id": "NTN-1"})
    settings.TAX_RATES = {"PK": "18"}  # a later change must not rewrite the first invoice
    o2 = _order(buyer, tree, surgical)
    for i, o in enumerate((o1, o2)):
        bs.record_payment(o, provider="manual", provider_ref=f"R{i}", amount_minor=o.amount_minor)
    a, b = Invoice.objects.order_by("id")
    assert a.number.endswith("000001") and b.number.endswith("000002")
    assert a.tax_rate == "16" and b.tax_rate == "18"
    assert a.buyer["name"] == "Acme Ltd" and a.buyer["tax_id"] == "NTN-1" and b.buyer["name"] == "inv_buyer"
    assert [ln["amount_minor"] for ln in a.lines] == [2900, 464]
    assert bs.issue_invoice(o1).pk == a.pk  # asking twice never makes a second invoice


def test_refund_issues_a_credit_note_and_never_edits_the_invoice(buyer, tree, surgical):
    o = _order(buyer, tree, surgical)
    bs.record_payment(o, provider="manual", provider_ref="R1", amount_minor=o.amount_minor)
    inv = Invoice.objects.get(order=o, kind="invoice")
    lines = list(inv.lines)
    mod = User.objects.create_user("modr", "m@x.org", PW)
    bs.refund_order(o, actor=mod)
    inv.refresh_from_db()
    cn = Invoice.objects.get(order=o, kind="credit_note")
    assert inv.lines == lines and cn.credit_for_id == inv.pk
    assert [ln["amount_minor"] for ln in cn.lines] == [-ln["amount_minor"] for ln in lines]
    assert cn.number != inv.number


def test_buyer_sees_only_own_invoice(buyer, tree, surgical):
    o = _order(buyer, tree, surgical)
    bs.record_payment(o, provider="manual", provider_ref="R1", amount_minor=o.amount_minor)
    mine, other = Client(), Client()
    mine.force_login(buyer)
    other.force_login(User.objects.create_user("stranger", "s@x.org", PW))
    r = mine.get(f"/account/orders/{o.ref}/invoice/")
    assert r.status_code == 200 and Invoice.objects.get(order=o).number in r.content.decode()
    assert other.get(f"/account/orders/{o.ref}/invoice/").status_code == 404


def test_revenue_report_by_currency_and_kind(buyer, tree, surgical, settings, db):
    o = _order(buyer, tree, surgical)
    bs.record_payment(o, provider="manual", provider_ref="R1", amount_minor=o.amount_minor, fees_minor=100)
    Product.objects.create(key="pk-sub", name="PKR sub", kind="subscription", price_minor=800000, currency="PKR")
    o2 = bs.create_order(buyer, Product.objects.get(key="pk-sub"), scope_path="pk.punjab.sialkot", concept=surgical)
    bs.record_payment(o2, provider="manual", provider_ref="R2", amount_minor=o2.amount_minor)
    rows = reporting.revenue_report()
    cur = {r["currency"]: r for r in rows}
    assert cur["USD"]["gross"] == 2900 and cur["USD"]["fees"] == 100 and cur["PKR"]["gross"] == 800000
    assert cur["USD"]["platform"] + cur["USD"]["contributors"] == cur["USD"]["net"]
    assert reporting.consolidated_usd(rows) is None  # no PKR rate configured
    settings.REPORT_RATES_TO_USD = {"PKR": "0.0036"}
    assert reporting.consolidated_usd(rows) == 2900 + 2880
    grant_role(buyer, "finance")
    c = Client()
    c.force_login(buyer)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    assert c.get("/staff/revenue/").status_code == 200
    assert c.get("/staff/revenue/?format=csv").content.decode().startswith("month,currency,kind")
