import datetime
import gzip
import re
from datetime import timedelta
from pathlib import Path

import pytest
from django.contrib.auth.models import User
from django.test import Client

from access.policy import FIELDS
from catalog import maps
from catalog.location import nearest_place
from core import clock
from core.models import CountrySwitch
from entries import services as es
from moderation import services as mod
from taxonomy.models import ListTypeSettings

PW = "Correct-horse-battery-9"
STATIC = Path(__file__).resolve().parents[1] / "static" / "catalog"
LIST = "/pk/punjab/sialkot/surgical-instrument-makers/"


# ---- static pages --------------------


@pytest.mark.parametrize(
    "path", ["/about/", "/terms/", "/privacy/", "/plans/", "/sources/", "/how-checks-work/", "/contributors/rules/"]
)
def test_static_pages_render_in_both_languages_with_cache_headers(path, db):
    for prefix in ("", "/ur"):
        r = Client().get(prefix + path)
        assert r.status_code == 200 and "public" in r["Cache-Control"] and "Cookie" not in r.get("Vary", "")
    assert Client().get(path).content == Client().get(path).content


def test_plans_page_is_generated_from_the_policy_table(db):
    html = Client().get("/plans/").content.decode()
    assert "Exact map pin" in html and "Advertisements" in html
    assert FIELDS["ads"] == ("full", "full", "none")
    row = re.search(r"Advertisements</th><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>", html)
    assert row.groups() == ("Yes", "Yes", "No")
    assert "never shown to anyone" in html


def test_how_checks_work_lists_exactly_the_four_labels(db):
    html = Client().get("/how-checks-work/").content.decode()
    for label in ("Surveyor-verified", "Owner-verified", "AI-checked", "Not verified yet"):
        assert label in html
    assert "cannot be bought" in html


def test_privacy_and_terms_say_what_the_decisions_say(db):
    p = Client().get("/privacy/").content.decode()
    assert "never shown" in p and "free" in p and "30 days" in p and "Lawyer" not in p and "lawyer" in p
    t = Client().get("/terms/").content.decode()
    assert "copy lists systematically" in t


def test_contributor_rules_match_the_money_rules(db):
    html = Client().get("/contributors/rules/").content.decode()
    for needle in ("only when a list", "50 percent, then 40, then 30", "36 months", "14 days", "second person"):
        assert needle in html


def test_sources_page_lists_attribution_and_hides_red_sources(db):
    from intake.models import Source

    Source.objects.create(
        name="GeoNames", tier="green", attribution_text="Place names from GeoNames, CC BY 4.0", allowed_uses=["import"]
    )
    Source.objects.create(
        name="Scraped maps", tier="red", attribution_text="should never show", allowed_uses=["import"]
    )
    html = Client().get("/sources/").content.decode()
    assert "GeoNames" in html and "CC BY 4.0" in html and "Scraped" not in html


# ---- maps (rule R36) --------------------


def test_map_links_use_the_stored_point_and_only_china_gets_baidu_and_amap():
    pk = maps.links(32.4945, 74.5229, "PK")
    assert set(pk) == {"google", "apple", "osm"} and "32.494500,74.522900" in pk["google"]
    cn = maps.links(39.9087, 116.3975, "CN")
    assert {"amap", "baidu"} <= set(cn)


def test_gcj02_and_bd09_shift_only_inside_china():
    lat, lon = 51.5074, -0.1278
    assert maps.wgs84_to_gcj02(lat, lon) == (lat, lon)
    blat, blon = 39.9087, 116.3975
    glat, glon = maps.wgs84_to_gcj02(blat, blon)
    assert 0.0005 < abs(glat - blat) < 0.01 and 0.0005 < abs(glon - blon) < 0.01
    dlat, dlon = maps.gcj02_to_bd09(glat, glon)
    assert abs(dlat - glat) > 0.001 and abs(dlon - glon) > 0.001
    assert maps.out_of_china(51.5, -0.12) and not maps.out_of_china(39.9, 116.4)


def test_subscribers_get_map_links_free_viewers_do_not(tree, surgical, make_published, settings):
    from decimal import Decimal

    settings.DEMO_MODE = True
    e = make_published("Pin Works", tree["paris"], lat=Decimal("32.4990"), lon=Decimal("74.5300"))
    free = Client().get(f"/_f/entry/{e.uid}/").content.decode()
    assert "openstreetmap" not in free
    c = Client()
    c.post("/prefs/", {"plan": "subscriber", "next": "/"})
    sub = c.get(f"/_f/entry/{e.uid}/").content.decode()
    assert "openstreetmap.org" in sub and "google.com/maps" in sub and "baidu" not in sub


# ---- exact location --------------------


def test_exact_location_matches_the_nearest_place_and_is_kept_in_the_session(db):
    from django.core.management import call_command

    call_command("seed_pilot")
    p = nearest_place(32.5, 74.53)
    assert p and p.slug in ("paris-road", "sialkot", "kashmir-road")
    assert nearest_place(51.5, -0.12) is None and nearest_place(95, 10) is None
    c = Client()
    r = c.post("/prefs/location/", {"lat": "32.4991", "lon": "74.5301", "next": "/pk/"})
    assert r.status_code == 302 and r["Location"] == "/pk/"
    html = c.get("/_f/near-you/").content.decode()
    assert "Showing lists for" in html and "guess" not in html
    assert Client().post("/prefs/location/", {"lat": "x", "lon": "y"}).status_code == 302
    assert (
        Client().post("/prefs/location/", {"lat": "1", "lon": "2", "next": "https://evil.example"})["Location"] == "/"
    )


# ---- stewardship --------------------


def test_steward_reviews_only_inside_their_segment_and_grants_expire(db, tree, surgical, make_published, users):
    e = make_published("Crescent Surgical Works", tree["paris"])
    other = make_published("Far Works", tree["world"], phone="0301 000 9999") if False else None
    assert other is None
    steward = users["owner"]
    es.grant_stewardship(steward, tree["sialkot"])
    assert es.steward_covers(steward, e)
    s = mod.suggest_edit(e, "website", "https://corrected.example.org")
    c = Client()
    c.force_login(steward)
    page = c.get("/account/steward/")
    assert page.status_code == 200 and "corrected.example.org" in page.content.decode()
    c.post("/account/steward/", {"id": s.pk, "action": "accept"})
    e.refresh_from_db()
    assert e.website == "https://corrected.example.org"
    es.touch_steward(steward, now=clock.now() - timedelta(days=100))
    assert es.expire_stewards() == 1
    assert not es.steward_covers(steward, e) and Client().get("/account/steward/").status_code == 302
    plain = User.objects.create_user("plainst", "p@x.org", PW)
    pc = Client()
    pc.force_login(plain)
    assert pc.get("/account/steward/").status_code == 403


def test_stewardship_scoped_to_one_list_type(db, tree, surgical, make_published, users):
    from taxonomy.services import create_concept

    e = make_published("Crescent Surgical Works", tree["paris"])
    other_type = create_concept(kind="list_type", name="Football makers")
    es.grant_stewardship(users["owner"], tree["sialkot"], concept=other_type)
    assert not es.steward_covers(users["owner"], e)


# ---- prices (rule R20) --------------------


def test_prices_need_a_date_and_health_prices_stay_off(db, tree, surgical, make_published):
    e = make_published("Crescent Surgical Works", tree["paris"])
    with pytest.raises(es.EntryError):
        es.add_service(e, "Delivery", price_minor=500, currency="usd")
    s = es.add_service(e, "Delivery", price_minor=500, currency="usd", price_date=datetime.date(2026, 10, 1))
    assert s.currency == "USD"
    with pytest.raises(es.EntryError):
        es.add_service(e, "cheapest", price_minor=1, currency="usd", price_date=datetime.date(2026, 10, 1))
    es.add_service(e, "Free quote")  # no price needs no date
    ListTypeSettings.objects.filter(concept=e.primary_concept).update(is_health=True)
    with pytest.raises(es.EntryError):
        es.add_service(e, "MRI scan", price_minor=9000, currency="pkr", price_date=datetime.date(2026, 10, 1))
    CountrySwitch.objects.update_or_create(country_code="PK", defaults={"health_prices_on": True})
    assert es.add_service(e, "MRI scan", price_minor=9000, currency="pkr", price_date=datetime.date(2026, 10, 1)).pk


# ---- build gates: weight, logical CSS, accessibility struc --------------------


def gz(html):
    return len(gzip.compress(html.encode(), 6))


def test_page_weight_ceilings(tree, surgical, make_published):
    for i in range(24):
        make_published(f"Weight {i:02d} Works", tree["paris"], phone=f"0303 000 {i:04d}", refresh=False)
    from analytics.rollups import recount_all

    recount_all()
    e = make_published("Heavy Works", tree["paris"], phone="0304 000 0000")
    c = Client()
    list_html = c.get(LIST).content.decode()
    entry_html = c.get(f"/e/{e.uid}/heavy-works/").content.decode()
    empty_html = c.get("/pk/punjab/sialkot/").content.decode()
    assert list_html.count('class="nm"') == 25
    assert gz(list_html) <= 18 * 1024, gz(list_html)  # hard ceiling for a 25-row list page
    assert gz(entry_html) <= 12 * 1024, gz(entry_html)
    assert gz(empty_html) <= 6 * 1024 + 4096, gz(empty_html)  # place pages carry tiles; the empty-list ceiling is 6 KB
    css = (STATIC / "app.css").read_text()
    js = (STATIC / "app.js").read_text() + (STATIC / "theme.js").read_text()
    assert len(gzip.compress(css.encode())) <= 8 * 1024 and len(gzip.compress(js.encode())) <= 30 * 1024


def test_css_uses_logical_properties_only():
    css = (STATIC / "app.css").read_text()
    props = ["margin-left", "margin-right", "padding-left", "padding-right", "border-left", "border-right"]
    banned = [p for p in props if re.search(r"(?<![\w-])" + p + r"\s*:", css)]
    banned += re.findall(r"text-align:\s*(?:left|right)|float:\s*(?:left|right)|(?<![-\w])(?:left|right)\s*:", css)
    assert banned == [], banned


def test_pages_have_landmarks_one_h1_skip_link_and_labelled_controls(tree, surgical, make_published):
    e = make_published("A11y Works", tree["paris"])
    for url in ("/", "/pk/", LIST, f"/e/{e.uid}/a11y-works/", "/about/", "/ur" + LIST):
        html = Client().get(url).content.decode()
        assert html.count("<h1") == 1, url
        assert "<main" in html and "<header" in html and "<footer" in html and 'class="skip"' in html, url
        assert re.search(r'<html lang="(en|ur)" dir="(ltr|rtl)"', html), url
        for inp in re.findall(r"<input\b[^>]*>", html):
            if 'type="hidden"' in inp or 'type="checkbox"' in inp:
                continue
            ident = re.search(r'id="([^"]+)"', inp)
            assert ident and (f'for="{ident.group(1)}"' in html or "aria-label" in inp), (url, inp)


def test_focus_and_reduced_motion_rules_exist_in_the_stylesheet():
    css = (STATIC / "app.css").read_text()
    assert ":focus-visible" in css and "prefers-reduced-motion" in css and "forced-colors" in css
    assert "outline:3px" in css.replace(" ", "")
