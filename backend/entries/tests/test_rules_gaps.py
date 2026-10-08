"""Rules the mutation check found untested: steward scope and expiry, health prices, service price rules, company page
editing rights and link ban, merge guards, expiry grace boundary."""

import datetime
from datetime import timedelta

import pytest
from django.contrib.auth.models import User

from accounts.roles import user_roles
from core import clock
from core.models import CountrySwitch
from entries import services as es
from entries.models import Entry, StewardGrant
from taxonomy.models import ListTypeSettings
from taxonomy.services import create_concept

PW = "Correct-horse-battery-9"
TODAY = datetime.date(2026, 10, 5)


# ---- stewards -----------------------------------------------------------------------------------------------------------------


def test_steward_covers_only_their_place_subtree_and_list_type(tree, surgical, make_published):
    u = User.objects.create_user("stew1", "s1@x.org", PW)
    other_type = create_concept(kind="list_type", name="Dental makers")
    in_city = make_published("In City", tree["paris"])
    other = make_published("Other Type", tree["paris"], concept=other_type, addons={})
    es.grant_stewardship(u, tree["sialkot"], concept=surgical)
    assert es.steward_covers(u, in_city)
    assert not es.steward_covers(u, other)  # right place, other list type
    es.grant_stewardship(u, tree["sialkot"])  # every list type there
    assert es.steward_covers(u, other)
    elsewhere = make_published("Elsewhere", tree["punjab"])
    assert not es.steward_covers(u, elsewhere)  # above the granted place
    outsider = User.objects.create_user("stew2", "s2@x.org", PW)
    assert not es.steward_covers(outsider, in_city)


def test_stewardship_expires_after_90_idle_days_and_the_role_goes_with_the_last_grant(tree, surgical):
    u = User.objects.create_user("stew3", "s3@x.org", PW)
    g1 = es.grant_stewardship(u, tree["sialkot"], concept=surgical)
    g2 = es.grant_stewardship(u, tree["punjab"])
    assert "steward" in user_roles(u)
    now = clock.now()
    StewardGrant.objects.filter(pk=g1.pk).update(last_active_at=now - timedelta(days=91))
    assert es.expire_stewards(now) == 1
    g1.refresh_from_db()
    assert g1.state == "expired" and "steward" in user_roles(u)  # another grant is still active
    es.touch_steward(u, now)
    assert es.expire_stewards(now + timedelta(days=89)) == 0  # touched, still inside the window
    assert es.expire_stewards(now + timedelta(days=91)) == 1
    assert "steward" not in user_roles(u) and g2


# ---- services and prices ---------------------------------------------------------------------------------------------------------


def test_service_price_rules(entry):
    with pytest.raises(es.EntryError, match="amount and a currency"):
        es.add_service(entry, "Cut", price_minor=-1, currency="PKR", price_date=TODAY)
    with pytest.raises(es.EntryError, match="amount and a currency"):
        es.add_service(entry, "Cut", price_minor=100, currency="", price_date=TODAY)
    with pytest.raises(es.EntryError, match="date"):
        es.add_service(entry, "Cut", price_minor=100, currency="PKR")
    with pytest.raises(es.EntryError, match="cheapest"):
        es.add_service(entry, "Cheapest", price_minor=100, currency="PKR", price_date=TODAY)
    ok = es.add_service(entry, " OEM ", price_minor=0, currency="pkr", price_date=TODAY)  # free is a valid price
    assert ok.name_text == "OEM" and ok.currency == "PKR"
    assert es.add_service(entry, "Quote on request").price_minor is None  # no price at all is fine


def test_health_prices_need_the_country_switch(tree, users):
    clinics = create_concept(kind="list_type", name="Eye clinics")
    ListTypeSettings.objects.filter(concept=clinics).update(is_health=True)
    e = es.create_entry(name="Eye Care", place=tree["paris"], primary_concept=clinics, created_by=users["adder"])
    with pytest.raises(es.EntryError, match="health"):
        es.add_service(e, "Cataract surgery", price_minor=50000, currency="PKR", price_date=TODAY)
    es.add_service(e, "Consultation")  # a service with no price is allowed
    CountrySwitch.objects.update_or_create(country_code="PK", defaults={"health_prices_on": True})
    assert es.add_service(e, "Cataract surgery", price_minor=50000, currency="PKR", price_date=TODAY).pk


# ---- company page editing ------------------------------------------------------------------------------------------------------


def test_only_the_owner_edits_the_company_page_and_links_are_banned_outside_products(entry, users):
    es.decide_claim(
        es.start_claim(entry, users["owner"], "documents", "I run it, licence 123456"), actor=users["mod"], approve=True
    )
    es.activate_company_plan(entry, days=30)
    with pytest.raises(es.GuardError, match="only the owner"):
        es.save_company_section(entry, users["adder"], "about", "We are great")
    with pytest.raises(es.EntryError, match="links"):
        es.save_company_section(entry, users["owner"], "about", "see https://spam.example")
    with pytest.raises(es.EntryError, match="links"):
        es.save_company_section(entry, users["owner"], "faq", "visit www.spam.example")
    assert es.save_company_section(
        entry, users["owner"], "products", "Catalogue: https://shop.example/c"
    ).pk  # products may link
    with pytest.raises(es.EntryError, match="unknown"):
        es.save_company_section(entry, users["owner"], "gossip", "x")
    with pytest.raises(es.EntryError, match="write something"):
        es.save_company_section(entry, users["owner"], "about", "   ")
    sec = es.save_company_section(entry, users["owner"], "about", "  Plain text  ")
    assert sec.body == "Plain text" and sec.state == "pending"  # every save waits for a moderator


def test_company_pages_are_not_for_people_or_child_services(tree, surgical, users):
    kids = create_concept(kind="list_type", name="Day care")
    ListTypeSettings.objects.filter(concept=kids).update(is_child_facing=True)
    e_kid = es.create_entry(name="Little Ones", place=tree["paris"], primary_concept=kids, created_by=users["adder"])
    person = es.create_entry(
        name="Dr P", place=tree["paris"], primary_concept=surgical, created_by=users["adder"], entity_type="person"
    )
    plain = es.create_entry(name="Biz", place=tree["paris"], primary_concept=surgical, created_by=users["adder"])
    assert not es.company_page_allowed(e_kid) and not es.company_page_allowed(person) and es.company_page_allowed(plain)


# ---- merging -----------------------------------------------------------------------------------------------------------------------


def test_merge_guards(tree, surgical, users, make_published):
    a = make_published("Alpha Works", tree["paris"], phone="0300 000 0001")
    b = make_published("Alpha Works Ltd", tree["paris"], phone="0300 000 0002")
    c = make_published("Gamma Works", tree["paris"], phone="0300 000 0003")
    with pytest.raises(es.EntryError, match="itself"):
        es.merge_entries(a, a)
    es.merge_entries(a, b)
    b.refresh_from_db()
    with pytest.raises(es.EntryError, match="itself or merge twice"):
        es.merge_entries(c, b)  # b is already merged away
    ae = Entry.objects.get(pk=a.pk)
    ae.country_code = "AE"
    with pytest.raises(es.EntryError, match="different countries"):
        es.merge_entries(ae, c)


# ---- expiry grace boundary ------------------------------------------------------------------------------------------------------


def test_expired_entry_returns_to_draft_only_after_the_grace_period(tree, surgical, users, make_published):
    from entries.models import VerificationCurrent

    e = make_published("Lapsing Works", tree["paris"], phone="0300 000 0010")
    last = clock.now() - timedelta(days=1)
    VerificationCurrent.objects.filter(entry=e).update(expires_at=last)
    from django.conf import settings

    grace = timedelta(days=settings.GRACE_DAYS)
    es.sweep_expired(last + grace)  # exactly at the end of grace: still allowed
    e.refresh_from_db()
    assert e.publish_state == "published"
    es.sweep_expired(last + grace + timedelta(seconds=1))
    e.refresh_from_db()
    assert e.publish_state == "draft"


def test_phone_numbers_in_pakistan_form(entry):
    assert es.normalize_contact("phone", "0300 123 4567", "PK") == "+923001234567"
    assert es.normalize_contact("phone", "0300 123 4567", "AE") == "03001234567"  # the rule is Pakistan's only
    assert es.normalize_contact("phone", "+971 50 123 4567", "PK") == "+971501234567"
    assert es.normalize_contact("phone", "300 123 4567", "PK") == "3001234567"  # no leading 0, nothing assumed
