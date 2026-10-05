import pytest
from django.test import Client

from analytics.models import Event
from catalog import search
from core.textfold import fold
from taxonomy.services import create_concept

SCOPE = "pk.punjab.sialkot"


@pytest.fixture
def data(tree, surgical, make_published, db):
    a = make_published("Crescent Surgical Works", tree["paris"], phone="0300 000 0001")
    b = make_published("Falcon Medical Instruments", tree["sialkot"], phone="0300 000 0002")
    c = make_published("كريسنت سرجيكل ورکس", tree["paris"], phone="0300 000 0003")
    return {"a": a, "b": b, "c": c, **tree}


def test_synonym_and_typo_find_the_list_type(data):
    assert surgical_in(search.concepts(fold("surgical instrument makers")))
    assert surgical_in(search.concepts(fold("surgical instruments manufacturers")))
    assert surgical_in(search.concepts(fold("surgical instrumnt makers")))  # typo
    assert not search.concepts(fold("football"))


def surgical_in(cs):
    return any(c.slug == "surgical-instrument-makers" for c in cs)


def test_places_found_in_both_scripts(data):
    assert any(p.slug == "sialkot" for p in search.places(fold("sialkot")))
    assert any(p.slug == "sialkot" for p in search.places(fold("سیالکوٹ")))
    assert any(p.slug == "sialkot" for p in search.places(fold("sialkott")))


def test_entries_found_by_name_typo_and_urdu_variant_only_inside_a_scope(data, tree):
    names = {e.name for e in search.entries(fold("crescent"), tree["sialkot"])}
    assert "Crescent Surgical Works" in names
    assert "Falcon Medical Instruments" in {e.name for e in search.entries(fold("falkon medical"), tree["sialkot"])}
    # the Urdu entry is written with Arabic yeh and kaf; the query uses the Farsi forms
    assert "كريسنت سرجيكل ورکس" in {e.name for e in search.entries(fold("کریسنت سرجیکل"), tree["sialkot"])}
    assert search.run("crescent")["entries"] == []  # unscoped never scans entry names


def test_drafts_never_appear(data, tree, surgical, users):
    from entries import services as es

    es.create_entry(
        name="Crescent Draft Co",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    assert "Crescent Draft Co" not in {e.name for e in search.entries(fold("crescent"), tree["sialkot"])}


def test_search_page_groups_and_zero_result_flow(data):
    c = Client()
    r = c.get("/search/", {"q": "surgical instrument", "scope": SCOPE})
    html = r.content.decode()
    assert r.status_code == 200 and "Surgical instrument makers" in html or "surgical-instrument-makers" in html
    assert r["Cache-Control"] == "private, no-store" and 'content="noindex,follow"' in html
    html = c.get("/search/", {"q": "crescent", "scope": SCOPE}).content.decode()
    assert "Crescent Surgical Works" in html and "Surveyor-verified" in html
    zero = c.get("/search/", {"q": "zzzzqqqq", "scope": SCOPE}).content.decode()
    assert "Nothing found" in zero and "/add/" in zero
    assert (
        Event.objects.filter(name="search_zero_result").count() == 1
        and Event.objects.filter(name="search").count() == 3
    )
    assert "at least two letters" in c.get("/search/", {"q": "a"}).content.decode()


def test_search_fragment_returns_only_rows(data):
    html = Client().get("/search/", {"q": "falcon", "scope": SCOPE, "fragment": "1"}).content.decode()
    assert "Falcon Medical Instruments" in html and "<html" not in html


def test_header_search_form_and_scope_hint_on_list_pages(data):
    html = Client().get("/pk/punjab/sialkot/surgical-instrument-makers/").content.decode()
    assert 'action="/search/"' in html and 'name="scope" value="pk.punjab.sialkot"' in html
    assert 'action="/ur/search/"' in Client().get("/ur/pk/punjab/sialkot/surgical-instrument-makers/").content.decode()


def test_events_are_a_closed_catalogue(db):
    from analytics.events import emit

    with pytest.raises(ValueError):
        emit("made_up_event")
    assert emit("quota_hit", None, key="names").name == "quota_hit"


def test_list_fragment_emits_list_view_without_contacts(data):
    Client().get("/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers")
    ev = Event.objects.get(name="list_view")
    assert (
        ev.props == {"path": "pk.punjab.sialkot", "type": "surgical-instrument-makers"} and len(ev.subject_hash) == 64
    )


def test_new_list_type_is_found_immediately(data):
    create_concept(kind="list_type", name="Football makers", synonyms=["soccer ball manufacturers"])
    assert any(c.slug == "football-makers" for c in search.concepts(fold("soccer ball")))
