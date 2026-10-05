import datetime

import pytest
from django.contrib.auth.models import User
from django.db import connection

from core.models import CountrySwitch
from entries import services as es
from intake.models import Source
from places.models import Place
from places.services import create_place
from taxonomy.models import Concept
from taxonomy.services import create_concept, seed_manufacturer_template


@pytest.fixture(autouse=True)
def fast_hashers(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def pg(db):
    if connection.vendor != "postgresql":
        pytest.skip("needs PostgreSQL (set POSTGRES_DB)")


@pytest.fixture
def tree(db):
    world = create_place(parent=None, level=Place.Level.WORLD, name="World", slug="world")
    pk = create_place(parent=world, level=Place.Level.COUNTRY, name="Pakistan", country_code="PK",
                      names=[("ur", "پاکستان")])
    punjab = create_place(parent=pk, level=Place.Level.ADMIN1, name="Punjab")
    sialkot = create_place(parent=punjab, level=Place.Level.CITY, name="Sialkot", names=[("ur", "سیالکوٹ")])
    paris = create_place(parent=sialkot, level=Place.Level.AREA, name="Paris Road")
    return dict(world=world, pk=pk, punjab=punjab, sialkot=sialkot, paris=paris)


@pytest.fixture
def surgical(db):
    tpl = seed_manufacturer_template()
    return create_concept(kind=Concept.Kind.LIST_TYPE, name="Surgical instrument makers", template=tpl,
                          synonyms=["surgical instruments manufacturers"])


@pytest.fixture
def users(db):
    return {n: User.objects.create_user(n, f"{n}@example.org", "pw-for-tests-only") for n in
            ("adder", "surveyor", "owner", "mod")}


@pytest.fixture
def green(db):
    return Source.objects.create(name="Owner submissions", tier="green", allowed_uses=["import", "agent_fetch", "display"])


@pytest.fixture
def web_source(db):
    return Source.objects.create(name="Open web page check", tier="amber", allowed_uses=["agent_fetch", "display"],
                                 reviewed_on=datetime.date(2026, 10, 1))


@pytest.fixture
def entry(tree, surgical, users):
    return es.create_entry(name="Crescent Surgical Works", place=tree["paris"], primary_concept=surgical,
                           created_by=users["adder"], website="https://example.org",
                           contacts=[("phone", "0300 123 4567")],
                           addons={"business_type": "manufacturer", "product_categories": ["scissors"]})


@pytest.fixture
def pk_open(db):
    return CountrySwitch.objects.create(country_code="PK", named_individuals_on=True)
