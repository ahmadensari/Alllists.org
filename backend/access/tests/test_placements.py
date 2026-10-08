from datetime import timedelta

import pytest
from django.test import Client

from access import placements as pl
from access.models import Ad, Placement
from billing import services as bs
from billing.models import Product
from core import clock
from entries import services as es

PW = "Correct-horse-battery-9"


@pytest.fixture
def owner_of(users):
    def make(entry):
        es.decide_claim(es.start_claim(entry, users["owner"], "documents", "mine"), actor=users["mod"], approve=True)
        return users["owner"]

    return make


def _html(client, url):
    return client.get(url).content.decode()


def test_sponsored_labelled_capped_and_checks_unchanged(tree, surgical, make_published):
    a = make_published("Alpha Works", tree["paris"], level="surveyor")
    b = make_published("Bravo Works", tree["paris"], level="surveyor")
    make_published("Charlie Works", tree["paris"], level="surveyor")
    # sponsoring an unchecked entry is allowed and shows as not verified; a check cannot be bought
    d = make_published("Delta Works", tree["paris"])
    d.verification_current.update(expires_at=clock.now() - timedelta(days=1))  # lapsed check: shows as not verified
    pl.create_placement(d, tree["sialkot"], surgical)
    pl.create_placement(a, tree["sialkot"], surgical)
    with pytest.raises(pl.PlacementError, match="no free sponsored slot"):
        pl.create_placement(b, tree["sialkot"], surgical)
    html = _html(Client(), "/pk/punjab/sialkot/surgical-instrument-makers/")
    section = html.split('class="sponsored-slot"')[1].split("</section>")[0]
    assert section.count("Sponsored") >= 2 and "Delta Works" in section and "Alpha Works" in section
    assert "Bravo Works" not in section and "Charlie Works" not in section
    assert "Not verified yet" in section or "level-none" in section or "chip" in section
    assert "How this list is ordered" in html
    # ordinary rows still alphabetical, with every entry in place
    rows = html.split('id="results"')[-1]
    assert (
        rows.index("Alpha Works") < rows.index("Bravo Works") < rows.index("Charlie Works") < rows.index("Delta Works")
    )


def test_placement_rules_entry_must_belong_and_be_open(tree, surgical, make_published, users):
    e = make_published("Alpha Works", tree["paris"])
    other = make_published("Beta Works", tree["paris"])
    with pytest.raises(pl.PlacementError):
        pl.create_placement(e, tree["world"], surgical)  # the whole world cannot be sponsored
    from places.services import create_place
    from places.models import Place

    elsewhere = create_place(parent=tree["punjab"], level=Place.Level.CITY, name="Lahore")
    with pytest.raises(pl.PlacementError, match="not in this place"):
        pl.create_placement(e, elsewhere, surgical)
    es.update_entry(other, actor=users["mod"], status="permanently_closed")
    with pytest.raises(pl.PlacementError, match="open entry"):
        pl.create_placement(other, tree["sialkot"], surgical)
    p = pl.create_placement(e, tree["sialkot"], surgical)
    assert p.level == "city" and p.slot == 1


def test_expiry_frees_the_slot_and_page_changes(tree, surgical, make_published):
    e = make_published("Alpha Works", tree["paris"])
    c = Client()
    url = "/pk/punjab/sialkot/surgical-instrument-makers/"
    before = c.get(url)
    p = pl.create_placement(e, tree["sialkot"], surgical)
    after = c.get(url)
    assert before["ETag"] != after["ETag"] and "sponsored-slot" in after.content.decode()
    Placement.objects.filter(pk=p.pk).update(ends_at=clock.now())
    assert pl.expire_due() == 1
    assert "sponsored-slot" not in c.get(url).content.decode()


def test_shared_page_is_identical_for_everyone_with_sponsored_rows(tree, surgical, make_published, users):
    e = make_published("Alpha Works", tree["paris"])
    pl.create_placement(e, tree["sialkot"], surgical)
    anon, logged = Client(), Client()
    logged.force_login(users["adder"])
    url = "/pk/punjab/sialkot/surgical-instrument-makers/"
    assert anon.get(url).content == logged.get(url).content


def test_rank_order_pays_creates_placement_and_refund_cancels(tree, surgical, make_published, users, owner_of):
    bs.seed_products()
    e = make_published("Alpha Works", tree["paris"])
    owner = owner_of(e)
    product = Product.objects.get(key="rank-city-month")
    with pytest.raises(bs.BillingError):
        bs.create_order(users["adder"], product, entry=e, concept=surgical, scope_path=tree["sialkot"].path)
    order = bs.create_order(owner, product, entry=e, concept=surgical, scope_path=tree["sialkot"].path)
    pay, _ = bs.record_payment(
        order, provider="manual", provider_ref="B1", amount_minor=order.amount_minor, actor=users["mod"]
    )
    assert Placement.objects.filter(order_ref=order.ref, state="active").count() == 1
    bs.refund_order(order, actor=users["mod"])
    assert Placement.objects.get(order_ref=order.ref).state == "cancelled"


def test_ads_free_viewers_only_text_only_approved_only(tree, surgical, make_published, users, owner_of):
    e = make_published("Alpha Works", tree["paris"])
    other = make_published("Beta Works", tree["paris"])
    owner = owner_of(e)
    with pytest.raises(pl.PlacementError, match="owner"):
        pl.submit_ad(users["adder"], e, "Buy now")
    with pytest.raises(pl.PlacementError, match="phone numbers"):
        pl.submit_ad(owner, e, "Call 0300 123 4567")
    ad = pl.submit_ad(
        owner, e, "Best scissors in Sialkot", "Made to order", scope_path=tree["sialkot"].path, concept=surgical
    )
    assert pl.pick_ad(tree["paris"].path, surgical.pk) is None  # pending ads never show
    pl.decide_ad(ad, actor=users["mod"], approve=True)
    assert pl.pick_ad(tree["paris"].path, surgical.pk).pk == ad.pk
    frag = Client().get(f"/_f/list/?path={tree['sialkot'].path}&type={surgical.slug}")
    assert "Best scissors in Sialkot" in frag.content.decode() and "Advertisement" in frag.content.decode()
    sub = Client()
    sub.force_login(users["adder"])
    from access.models import Plan
    from access import services as acs

    Plan.objects.get_or_create(key="subscriber_scope", defaults={"name": "s"})
    acs.grant_subscription(
        users["adder"], Plan.objects.get(key="subscriber_scope"), scope_path="", concept=None, days=30
    )
    assert (
        "Best scissors" not in sub.get(f"/_f/list/?path={tree['sialkot'].path}&type={surgical.slug}").content.decode()
    )
    r = Client().get(f"/go/ad/{ad.pk}/")
    assert r.status_code == 302 and "/e/" in r["Location"]
    assert Ad.objects.get(pk=ad.pk).clicks == 1
    assert other  # keep fixture used
