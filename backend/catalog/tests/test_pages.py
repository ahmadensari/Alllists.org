import json
import re

import pytest
from django.test import Client

from core.models import CountrySwitch
from entries import services as es

LIST = "/pk/punjab/sialkot/surgical-instrument-makers/"
PHONE_PARTS = ("300 000 0000", "3000000000", "923000000000", "0300 000 0000")


@pytest.fixture
def demo(settings):
    settings.DEMO_MODE = True


@pytest.fixture
def world_data(tree, surgical, make_published, users):
    a = make_published("Crescent Surgical Works", tree["paris"], phone="0300 000 0000")
    b = make_published("Falcon Medical Instruments", tree["sialkot"], level="surveyor", phone="0300 000 0001")
    return {"a": a, "b": b, **tree}


def subscriber_client(settings):
    c = Client()
    c.post("/prefs/", {"plan": "subscriber", "next": "/"})
    return c


def own_place_client(place):
    c = Client()
    c.post("/prefs/", {"place": place.uid, "next": "/"})
    return c


def test_pages_render_and_resolve(world_data):
    c = Client()
    assert c.get("/").status_code == 200
    assert c.get("/pk/").status_code == 200 and c.get("/pk/punjab/sialkot/").status_code == 200
    assert c.get(LIST).status_code == 200
    assert c.get("/pk/punjab/sialkot/nonsense/").status_code == 404
    assert c.get("/zz/").status_code == 404
    assert b"Page not found" in c.get("/zz/").content


def test_titles_canonical_and_hreflang(world_data):
    html = Client().get(LIST).content.decode()
    assert "<title>Surgical instrument makers in Sialkot – AllLists</title>" in html
    assert 'rel="canonical" href="http://testserver/pk/punjab/sialkot/surgical-instrument-makers/"' in html
    assert 'hreflang="ur" href="http://testserver/ur/pk/punjab/sialkot/surgical-instrument-makers/"' in html
    e = world_data["a"]
    entry_html = Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "<title>Crescent Surgical Works – Surgical instrument makers in Paris Road – AllLists</title>" in entry_html


def test_shell_identical_for_every_viewer_and_cacheable(world_data, demo, settings):
    """R05: location and plan never change the bytes at an address."""
    anon = Client().get(LIST)
    sub = subscriber_client(settings)
    guessed = Client()
    a = anon.content
    assert sub.get(LIST).content == a
    assert guessed.get(LIST, HTTP_CF_IPCOUNTRY="PK", HTTP_CF_IPCITY="Sialkot").content == a
    assert guessed.get(LIST, HTTP_CF_IPCOUNTRY="AE", HTTP_CF_IPCITY="Dubai").content == a
    assert "Cookie" not in anon.get("Vary", "")
    assert "public" in anon["Cache-Control"] and "s-maxage" in anon["Cache-Control"]
    assert anon["X-Template-Version"] == "1"
    etag = anon["ETag"]
    again = Client().get(LIST, HTTP_IF_NONE_MATCH=etag)
    assert again.status_code == 304


def test_entry_shell_identical_for_every_viewer(world_data, demo, settings):
    e = world_data["a"]
    url = f"/e/{e.uid}/crescent-surgical-works/"
    anon = Client().get(url).content
    assert subscriber_client(settings).get(url).content == anon
    assert "Cookie" not in Client().get(url).get("Vary", "")


def test_no_redirect_by_location(world_data):
    r = Client().get(LIST, HTTP_CF_IPCOUNTRY="AE", HTTP_CF_IPCITY="Dubai")
    assert r.status_code == 200


def test_contacts_never_rendered_anywhere(world_data, demo, settings):
    e = world_data["a"]
    sub = subscriber_client(settings)
    urls = [
        "/",
        "/pk/",
        LIST,
        f"/e/{e.uid}/crescent-surgical-works/",
        "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers",
        f"/_f/entry/{e.uid}/",
        "/_f/near-you/",
        "/ur" + LIST,
    ]
    for client in (Client(), sub):
        for url in urls:
            body = client.get(url).content.decode()
            assert not any(p in body for p in PHONE_PARTS), url
            assert "value_enc" not in body and "value_hash" not in body


def test_draft_hidden_and_counts_say_awaiting(world_data, tree, surgical, users):
    from analytics.rollups import recount_all

    draft = es.create_entry(
        name="Hidden Draft Co",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    recount_all()
    html = Client().get(LIST).content.decode()
    assert "Hidden Draft Co" not in html
    assert "2 published, 1 awaiting verification" in html
    assert Client().get(f"/e/{draft.uid}/hidden-draft-co/").status_code == 404


def test_rows_have_no_position_numbers_and_no_not_stated(world_data):
    html = Client().get(LIST).content.decode()
    assert "<ol" not in html.split('id="results"')[1].split("</ul>")[0]
    assert "Not stated" not in html and "not stated" not in html
    assert re.search(r'class="nm"[^>]*>\s*\d+[.)]', html) is None


def test_list_shell_is_names_only_safe(world_data):
    """The shared shell shows name, area and check; richer free fields arrive through the private fragment."""
    html = Client().get(LIST).content.decode()
    assert "Crescent Surgical Works" in html and "Paris Road" in html and "Surveyor-verified" in html
    assert "scissors" not in html and "example.org" not in html


def test_urdu_prefix_rtl_and_prefixed_links(world_data):
    html = Client().get("/ur" + LIST).content.decode()
    assert 'lang="ur"' in html and 'dir="rtl"' in html
    assert 'href="/ur/pk/punjab/sialkot/"' in html or 'href="/ur/pk/"' in html
    assert 'hreflang="en"' in html and 'href="/pk/punjab/sialkot/surgical-instrument-makers/"' in html  # switch back
    assert Client().get("/ur/").status_code == 200


def test_robots_meta_rules(world_data, tree, make_published, surgical):
    c = Client()
    assert 'content="noindex,follow"' in c.get(LIST).content.decode()  # switch off
    CountrySwitch.objects.create(country_code="PK", indexing_on=True)
    assert 'content="noindex,follow"' in c.get(LIST).content.decode()  # only 2 verified, threshold 10
    for i in range(9):
        make_published(f"Maker {i} Works", tree["paris"], phone=f"0301 000 00{i}0", refresh=False)
    from analytics.rollups import recount_all

    recount_all()
    html = c.get(LIST).content.decode()
    assert 'content="index,follow"' in html
    assert 'content="noindex,follow"' in c.get(LIST + "?sort=checked").content.decode()  # filters and sorts never index
    assert 'content="noindex,follow"' in c.get(LIST + "?area=paris-road").content.decode()


def test_robots_txt_does_not_block_thin_pages(client):
    body = client.get("/robots.txt").content.decode()
    assert "Disallow: /_f/" in body and "Disallow: /admin/" in body
    assert "Disallow: /pk" not in body and "Disallow: /\n" not in body and "Sitemap:" in body


def test_sitemap_lists_only_indexable_pages(world_data, tree, make_published, client):
    assert b"<loc>" not in client.get("/sitemap.xml").content
    CountrySwitch.objects.create(country_code="PK", indexing_on=True)
    for i in range(9):
        make_published(f"Maker {i} Works", tree["paris"], phone=f"0301 000 00{i}0", refresh=False)
    from analytics.rollups import recount_all

    recount_all()
    idx = client.get("/sitemap.xml").content.decode()
    assert "/sitemaps/pk-1.xml" in idx
    shard = client.get("/sitemaps/pk-1.xml").content.decode()
    assert "http://testserver/pk/punjab/sialkot/surgical-instrument-makers/" in shard
    assert client.get("/sitemaps/pk-2.xml").status_code == 404


def test_fragments_are_private_noindex_and_never_cached(world_data):
    r = Client().get("/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers")
    assert r["Cache-Control"] == "private, no-store" and "Cookie" in r["Vary"] and r["X-Robots-Tag"] == "noindex"
    assert Client().get("/_f/near-you/")["Cache-Control"] == "private, no-store"


def test_wider_than_own_place_is_names_only_for_free(world_data):
    path = "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers"
    free_no_place = Client().get(path).content.decode()
    assert "names only" in free_no_place.lower() and "detail-" not in free_no_place
    own = own_place_client(world_data["sialkot"]).get(path).content.decode()
    assert "detail-" in own and "scissors" in own and "names only" not in own.lower()
    other = (
        own_place_client(world_data["sialkot"])
        .get("/_f/list/?path=pk&type=surgical-instrument-makers")
        .content.decode()
    )
    assert "names only" in other.lower()


def test_subscriber_fragment_has_full_specialities_and_no_ads(world_data, demo, settings):
    path = "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers"
    free = own_place_client(world_data["sialkot"]).get(path).content.decode()
    assert 'id="ad-slot"' in free
    sub = subscriber_client(settings).get(path).content.decode()
    assert 'id="ad-slot"' not in sub


def test_entry_fragment_free_locked_subscriber_sees_details_but_never_contacts(world_data, demo, settings):
    e = world_data["a"]
    free = Client().get(f"/_f/entry/{e.uid}/").content.decode()
    assert "example.org" not in free and "What subscribers also see" in free
    sub = subscriber_client(settings).get(f"/_f/entry/{e.uid}/").content.decode()
    assert "https://example.org/crescent" in sub and "What subscribers also see" not in sub
    assert not any(p in sub for p in PHONE_PARTS)
    assert 'id="ad-slot"' not in sub


def test_demo_plan_switch_is_off_outside_demo(world_data, settings):
    settings.DEMO_MODE = False
    c = Client()
    c.post("/prefs/", {"plan": "subscriber", "next": "/"})
    e = world_data["a"]
    assert "example.org" not in c.get(f"/_f/entry/{e.uid}/").content.decode()


def test_prefs_rejects_open_redirect(world_data):
    r = Client().post("/prefs/", {"next": "https://evil.example/"})
    assert r["Location"] == "/"


def test_near_you_uses_edge_guess_and_says_so(world_data):
    html = Client().get("/_f/near-you/", HTTP_CF_IPCOUNTRY="PK", HTTP_CF_IPCITY="Sialkot").content.decode()
    assert "guess from your connection" in html and "Sialkot" in html
    assert "could not tell" in Client().get("/_f/near-you/").content.decode()


def test_closed_entry_shows_notice_and_no_message_button(world_data, users):
    e = world_data["a"]
    open_frag = Client().get(f"/_f/entry/{e.uid}/").content.decode()
    assert "Message this business" in open_frag
    es.update_entry(e, status="permanently_closed")
    html = Client().get(f"/e/{e.uid}/crescent-surgical-works/").content.decode()
    assert "This business is closed" in html
    assert "Message this business" not in Client().get(f"/_f/entry/{e.uid}/").content.decode()


def test_old_slug_and_merged_entries_redirect(world_data, tree, surgical, users):
    e, other = world_data["a"], world_data["b"]
    assert Client().get(f"/e/{e.uid}/wrong-slug/").status_code == 301
    assert Client().get(f"/e/{e.uid}/").status_code == 301
    es.merge_entries(e, other)
    r = Client().get(f"/e/{other.uid}/falcon-medical-instruments/")
    assert r.status_code == 301 and r["Location"].startswith(f"/e/{e.uid}/")


def test_individual_entries_have_no_share_controls_and_no_index(world_data, tree, surgical, users, pk_open):
    from analytics.rollups import recount_all

    p = es.create_entry(
        name="Dr Example",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        entity_type="person",
        website="https://dr.example.org",
        addons={"business_type": "trader", "product_categories": ["a"]},
    )
    es.record_consent(p, status="consented", method="form", wording_version="v1")
    es.record_verification(
        p, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    recount_all()
    html = Client().get(f"/e/{p.uid}/dr-example/").content.decode()
    assert "data-copy" not in html and "wa.me" not in html and 'content="noindex,follow"' in html


def test_new_share_channel_appears_on_list_and_entry_without_template_change(world_data, monkeypatch):
    """Rule R25: one registry row reaches every page."""
    from catalog import share

    monkeypatch.setattr(
        share,
        "CHANNELS",
        share.CHANNELS
        + [
            {
                "id": "telegram",
                "label": "Telegram",
                "group": "more",
                "kind": "link",
                "url": lambda c: "https://t.me/share/url?url=" + c["url"],
            }
        ],
    )
    e = world_data["a"]
    for url in (LIST, f"/e/{e.uid}/crescent-surgical-works/"):
        assert "t.me/share/url" in Client().get(url).content.decode()


def test_jsonld_is_valid_and_has_no_contacts(world_data):
    e = world_data["a"]
    for url in (LIST, f"/e/{e.uid}/crescent-surgical-works/"):
        html = Client().get(url).content.decode()
        block = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1)
        data = json.loads(block)
        assert data["@context"] == "https://schema.org"
        assert not any(p in block for p in PHONE_PARTS) and "telephone" not in block


def test_list_page_queries_do_not_grow_with_rows(world_data, tree, make_published):
    """No N+1: the query count is the same for 2 rows and for a full page of 25."""
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    from analytics.rollups import recount_all

    def count():
        with CaptureQueriesContext(connection) as ctx:
            r = Client().get(LIST)
        return len(ctx), r

    few, _ = count()
    for i in range(24):
        make_published(f"Budget {i:02d} Works", tree["paris"], phone=f"0302 000 {i:04d}", refresh=False)
    recount_all()
    many, r = count()
    assert many == few and many <= 25
    html = r.content.decode()
    assert html.count('class="nm"') == 25 and "page-fragments" in html and "Next page" in html
    assert Client().get(LIST + "?page=2").status_code == 200
