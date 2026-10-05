import datetime

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client

from lists.models import Check, Contribution, Enquiry, Entry, ListType, Place, Report, Sale
from lists.share import build

LIST_URL = "/p/pakistan/punjab/sialkot/l/surgical-instrument-makers/"


@pytest.fixture
def demo(db):
    call_command("seed_demo")


def sub_client():
    c = Client()
    c.post("/prefs/", {"plan": "subscriber"})
    return c


def first_pk(name="Crescent Surgical Works"):
    return Entry.objects.get(name=name).pk


def test_demo_seed_is_idempotent(demo):
    call_command("seed_demo")
    assert Entry.objects.count() == 6


def test_home_and_place_pages(demo):
    c = Client()
    assert b"Pakistan" in c.get("/").content
    r = c.get("/p/pakistan/punjab/sialkot/")
    assert r.status_code == 200 and b"Surgical instrument makers" in r.content
    assert c.get("/p/nowhere/").status_code == 404


def test_contacts_never_shown_to_anyone(demo, settings):
    settings.DEMO_MODE = True
    pk = first_pk()
    for client in (Client(), sub_client()):
        for url in (LIST_URL, f"/e/{pk}/"):
            body = client.get(url).content.decode()
            assert "+92 300" not in body and "0000000" not in body


def test_free_viewer_sees_limited_fields(demo, settings):
    settings.DEMO_MODE = True
    pk = first_pk()
    body = Client().get(f"/e/{pk}/").content.decode()
    assert "Plot 10" not in body and "example.org" not in body
    assert "+1 more" in body  # 4 specialities, free sees 3
    sub = sub_client().get(f"/e/{pk}/").content.decode()
    assert "Plot 10" in sub and "example.org" in sub and "Family firm" in sub


def test_company_page_extra_section_only_for_company(demo, settings):
    settings.DEMO_MODE = True
    basic = first_pk("Royal Steel Instruments")
    assert b"Family firm" not in sub_client().get(f"/e/{basic}/").content


def test_wider_list_is_names_only_for_free(demo, settings):
    settings.DEMO_MODE = True
    free = Client().get(LIST_URL).content.decode()  # no own place known: wider scope
    assert "Crescent Surgical Works" in free and "Manufacturer" not in free
    own = Client()
    own.post("/prefs/", {"place": Place.objects.get(slug="sialkot").pk})
    assert b"Manufacturer" in own.get(LIST_URL).content


def test_location_guess_from_edge_headers(demo):
    r = Client().get("/", HTTP_CF_IPCOUNTRY="PK", HTTP_CF_IPCITY="Sialkot")
    assert r.status_code == 200 and b"Guessed" in r.content


def test_urdu_switch_sets_rtl(demo):
    c = Client()
    c.post("/prefs/", {"lang": "ur"})
    assert 'dir="rtl"' in c.get("/").content.decode()


def test_prefs_rejects_open_redirect(demo):
    r = Client().post("/prefs/", {"lang": "en", "next": "https://evil.example/"})
    assert r["Location"] == "/"


def test_plan_switch_disabled_outside_demo(demo, settings):
    settings.DEMO_MODE = False
    c = Client()
    c.post("/prefs/", {"plan": "subscriber"})
    assert b"Plot 10" not in c.get(f"/e/{first_pk()}/").content


def test_enquiry_requires_subscriber(demo, settings):
    settings.DEMO_MODE = True
    data = {"entries": str(first_pk()), "reply_to": "a@b.co", "message": "Need 500 scissors"}
    Client().post("/enquiry/", data)
    assert Enquiry.objects.count() == 0
    sub_client().post("/enquiry/", data)
    assert Enquiry.objects.count() == 1


def test_report_and_claim(demo):
    c = Client()
    pk = first_pk()
    c.post(f"/e/{pk}/report/", {"note": "closed"})
    c.post(f"/e/{pk}/claim/", {"contact": "me@x.co"})
    assert Report.objects.filter(kind="report").count() == 1 and Report.objects.filter(kind="claim").count() == 1
    assert c.post(f"/e/{pk}/bogus/").status_code == 404


def test_search_and_area_filter(demo):
    c = Client()
    c.post("/prefs/", {"place": Place.objects.get(slug="sialkot").pk})
    body = c.get(LIST_URL + "?q=falcon").content.decode()
    assert "Falcon Medical" in body and "Crescent" not in body
    body = c.get(LIST_URL + "?area=kashmir-road").content.decode()
    assert "Falcon" in body and "Crescent" not in body


def test_share_registry_adds_utm():
    links = build("T", "line", "https://x.org/a", "list_share")
    assert {"whatsapp", "copy", "facebook", "email", "linkedin", "x"} == {c["id"] for c in links}
    assert all("utm_campaign=list_share" in c["copy"] for c in links)
    assert not any(c["id"] == "x" for c in build("T", "l", "https://x.org", "c", hide=("x",)))


def test_contributor_rate_locked_and_sale_distribution(demo, settings):
    e = Entry.objects.get(name="Crescent Surgical Works")
    assert e.contribution.rate_percent == 50 and e.contribution.phase == 1
    settings.CURRENT_PHASE = 3
    lt = ListType.objects.get(slug="surgical-instrument-makers")
    new = Entry.objects.create(name="Late Entry", place=e.place, entry_type="Trader")
    new.list_types.add(lt)
    Contribution.lock(new, User.objects.get(username="contributor1"))
    assert new.contribution.rate_percent == 30 and Entry.objects.get(pk=e.pk).contribution.rate_percent == 50
    sale = Sale.objects.create(place=Place.objects.get(slug="sialkot"), list_type=lt, amount_cents=70000)
    lines = sale.distribute()
    assert len(lines) == 7 and sale.distribute() == []
    by_entry = {ln.entry_id: ln.amount_cents for ln in lines}
    assert by_entry[e.pk] == 5000 and by_entry[new.pk] == 3000


def test_best_level(demo):
    e = Entry.objects.get(name="Crescent Surgical Works")
    Check.objects.create(entry=e, level="ai", checked_on=datetime.date.today())
    assert e.best_level() == "surveyor"
    assert Entry.objects.get(name="Unity Surgical Co").best_level() == "none"


def test_healthz_and_404(demo):
    c = Client()
    assert c.get("/healthz").content == b"ok"
    assert c.get("/e/99999/").status_code == 404
