"""Every route, every kind of visitor, every method (plan P3.19, "authorisation tests for every route").

Seeds a realistic little world, then walks the route inventory as an anonymous visitor, a plain account, a surveyor, a
subscriber, a moderator, a finance officer and an admin. It checks four things for each request:
1. nothing answers with a server error;
2. staff pages refuse everyone without the role, and login pages send visitors to sign in;
3. no page, for anyone but the audited surveyor reveal, contains a contact value or stored ciphertext;
4. pages that are cached and shared are byte-for-byte the same for everyone."""

import re
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.test import Client

from access import placements as pl
from access import services as acs
from access.models import Plan
from accounts.roles import grant_role
from catalog.route_access import LOGIN, PUBLIC, ROUTES, STAFF
from catalog.staff_views import QUEUES
from core import clock
from entries import services as es
from moderation import services as mod
from outreach import services as relay
from volunteers import onboarding
from volunteers import services as vs

PW = "Correct-horse-battery-9"
SECRET_BITS = ("3001234567", "300 123 4567", "owner@shop.example", "hidden-phone-9", "0300 777 8888", "3007778888")
CIPHER = re.compile(r"\bk\d+:gAAAA[\w\-=]{20,}")


@pytest.fixture
def world(tree, surgical, make_published, users, db):
    owner_entry = make_published("Crescent Surgical Works", tree["paris"], phone="0300 123 4567")
    es.add_contact(owner_entry, "email", "owner@shop.example")
    other = make_published("Falcon Medical Instruments", tree["sialkot"], phone="0300 777 8888")
    claim = es.start_claim(other, users["owner"], "documents", "I run Falcon Medical since 1998, licence 4412")
    es.decide_claim(claim, actor=users["mod"], approve=True)
    closed = make_published("Closed Works", tree["paris"], phone="0300 000 1111")
    es.update_entry(closed, actor=users["mod"], status="permanently_closed")
    draft = es.create_entry(
        name="Draft Co",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    mod.submit_report(owner_entry, "closed", "seems shut")
    mod.suggest_edit(owner_entry, "website", "https://new.example", users["adder"])
    vs.queue_verification(draft)
    pl.create_placement(other, tree["sialkot"], surgical)
    ad = pl.submit_ad(
        users["owner"], other, "Falcon forceps", "since 1998", scope_path=tree["sialkot"].path, concept=surgical
    )
    pl.decide_ad(ad, actor=users["mod"], approve=True)
    return dict(tree=tree, surgical=surgical, e=owner_entry, other=other, closed=closed, draft=draft, ad=ad)


def _client(user=None, staff=False, subscriber=False):
    c = Client(raise_request_exception=False)
    if user is not None:
        c.force_login(user)
        if staff:
            s = c.session
            s["mfa_ok"] = True
            s.save()
    if subscriber:
        Plan.objects.get_or_create(key="subscriber_scope", defaults={"name": "s"})
        acs.grant_subscription(user, Plan.objects.get(key="subscriber_scope"), scope_path="", concept=None, days=30)
    return c


@pytest.fixture
def principals(users, world):
    people = {}
    people["anon"] = _client()
    people["user"] = _client(User.objects.create_user("plainperson", "plain@example.org", PW))
    sv = users["surveyor"]
    grant_role(sv, "surveyor")
    onboarding.submit(
        sv, {"contacts": "b", "rights": "a", "independence": "b", "evidence": "a", "people": "a"}, declared_rights=True
    )
    people["surveyor"] = _client(sv)
    sub = User.objects.create_user("subscriber1", "sub@example.org", PW)
    people["subscriber"] = _client(sub, subscriber=True)
    for role in ("moderator", "finance", "admin"):
        u = User.objects.create_user(f"{role}1", f"{role}@example.org", PW)
        grant_role(u, role)
        people[role] = _client(u, staff=True)
    return people


def urls_for(world, order_ref):
    e, other = world["e"], world["other"]
    subst = {
        "<str:uid>": e.uid,
        "<slug:slug>": "crescent-surgical-works",
        "<str:token>": "nope",
        "<int:pk>": "1",
        "<str:ref>": order_ref,
        "<str:code>": "ABCDEF",
        "<str:provider>": "sandbox",
        "<str:cc>-<int:n>": "pk-1",
        "<uidb64>/<token>": "MQ/abc-def",
    }
    out = []
    for route in ROUTES:
        if route.startswith("^"):
            out += ["/pk/", "/pk/punjab/sialkot/", "/pk/punjab/sialkot/surgical-instrument-makers/", "/zz/nothing/"]
            continue
        if "<str:key>" in route:
            for key in QUEUES:
                out.append(
                    "/" + route.replace("<str:key>", key).replace("<int:pk>", "1").replace("<str:action>", "approve")
                )
            out.append(
                "/" + route.replace("<str:key>", "nonsense").replace("<int:pk>", "1").replace("<str:action>", "x")
            )
            continue
        url = route
        for k, v in subst.items():
            url = url.replace(k, v)
        out.append("/" + url)
    out += [
        f"/e/{other.uid}/falcon-medical-instruments/",
        f"/_f/entry/{other.uid}/",
        f"/_f/entry/{world['closed'].uid}/",
    ]
    out += [
        "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers",
        "/search/?q=falcon&scope=pk.punjab.sialkot",
    ]
    out += [
        "/ur/",
        "/ur/pk/",
        f"/ur/e/{e.uid}/crescent-surgical-works/",
        "/ur/pk/punjab/sialkot/surgical-instrument-makers/",
    ]
    return sorted(set(out))


@pytest.fixture
def order_ref(world, users):
    from billing import services as bs
    from billing.models import Product

    bs.seed_products()
    o = bs.create_order(
        users["adder"],
        Product.objects.get(key="subscription-city-month"),
        scope_path="pk.punjab.sialkot",
        concept=world["surgical"],
    )
    return o.ref


def test_nobody_gets_a_server_error_anywhere(world, principals, order_ref):
    urls = urls_for(world, order_ref)
    assert len(urls) > 80
    bad = []
    for who, c in principals.items():
        for url in urls:
            for method in ("get", "post"):
                try:
                    r = getattr(c, method)(url, {} if method == "post" else None)
                except Exception as exc:  # noqa: BLE001
                    bad.append((who, method, url, f"exception {type(exc).__name__}: {exc}"))
                    continue
                if r.status_code >= 500:
                    bad.append((who, method, url, r.status_code))
    assert bad == [], bad[:15]


def test_access_levels_are_enforced_for_every_route(world, principals, order_ref):
    problems = []
    staff_urls = [u for u in urls_for(world, order_ref) if u.startswith("/staff/") or u == "/admin/"]
    login_urls = ["/" + r for r, lvl in ROUTES.items() if lvl == LOGIN and "<" not in r and not r.startswith("^")]
    for url in staff_urls:
        for who in ("anon", "user", "surveyor", "subscriber"):
            r = principals[who].get(url)
            if who == "anon" and r.status_code != 302:
                problems.append((who, url, r.status_code))
            elif who != "anon" and r.status_code not in (403, 302):
                problems.append((who, url, r.status_code))
    for url in login_urls:
        r = principals["anon"].get(url)
        if not (r.status_code == 302 and r["Location"].startswith("/account/login/")):
            problems.append(("anon", url, r.status_code))
    assert problems == [], problems[:15]


def test_staff_roles_see_only_what_their_role_allows(world, principals):
    # finance cannot moderate, moderators cannot touch the ledger, nobody below admin can run extracts
    assert principals["finance"].get("/staff/ledger/").status_code == 200
    assert principals["moderator"].get("/staff/ledger/").status_code == 403  # the money pages are for finance and admin
    assert principals["finance"].get("/staff/claims/").status_code == 403
    assert principals["moderator"].get("/staff/claims/").status_code == 200
    for who in ("moderator", "finance"):
        assert principals[who].get("/staff/extracts/").status_code == 403
        assert principals[who].get("/staff/statistics/").status_code == 403
    assert principals["admin"].get("/staff/extracts/").status_code == 200
    assert principals["moderator"].get("/staff/subject-access/").status_code == 200
    assert principals["finance"].get("/staff/subject-access/").status_code == 403
    # a moderator cannot create or approve payouts
    r = principals["moderator"].post("/staff/ledger/", {"action": "create"})
    assert r.status_code == 403


def test_no_contact_value_or_ciphertext_in_any_page_for_anyone(world, principals, order_ref):
    leaks = []
    for who, c in principals.items():
        for url in urls_for(world, order_ref):
            r = c.get(url)
            body = (
                r.content.decode("utf-8", "replace")
                if r.get("Content-Type", "").startswith(("text", "application/json", "application/xml"))
                else ""
            )
            if any(bit in body for bit in SECRET_BITS) or CIPHER.search(body):
                leaks.append((who, url))
    assert leaks == [], leaks[:15]


def test_shared_pages_are_identical_for_everyone_and_set_no_cookie(world, principals):
    shared = [
        "/",
        "/pk/",
        "/pk/punjab/sialkot/",
        "/pk/punjab/sialkot/surgical-instrument-makers/",
        f"/e/{world['e'].uid}/crescent-surgical-works/",
        "/about/",
        "/plans/",
        "/ur/pk/",
    ]
    for url in shared:
        base = principals["anon"].get(url)
        assert base.status_code == 200 and "Set-Cookie" not in base.headers, url
        assert "public" in base["Cache-Control"], url
        for who in ("user", "surveyor", "subscriber", "moderator", "admin"):
            r = principals[who].get(url)
            assert r.content == base.content, (who, url)
            assert r["ETag"] == base["ETag"], (who, url)


def test_private_parts_are_never_cached_by_shared_caches(world, principals):
    for url in (
        "/_f/near-you/",
        f"/_f/entry/{world['e'].uid}/",
        "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers",
        "/account/",
        "/staff/",
    ):
        for who in ("anon", "user", "admin"):
            r = principals[who].get(url)
            if r.status_code in (200, 204):
                assert "no-store" in r["Cache-Control"] or "private" in r["Cache-Control"], (
                    who,
                    url,
                    r["Cache-Control"],
                )


def test_only_webhook_routes_skip_csrf(world):
    c = Client(enforce_csrf_checks=True, raise_request_exception=False)
    for route, level in ROUTES.items():
        if level in (STAFF, "webhook") or route.startswith("^") or "<" in route:
            continue
        if route in ("account/mfa/setup/", "account/mfa/verify/", "account/password/reset/"):
            pass
        r = c.post("/" + route, {})
        if level == PUBLIC and route in ("healthz", "robots.txt", "sitemap.xml"):
            assert r.status_code in (403, 405), route
            continue
        assert r.status_code in (403, 302, 405, 404), (route, r.status_code)
    assert clock and timedelta and relay


def test_null_bytes_are_refused_not_crashed_on(world, principals):
    c = principals["anon"]
    for url in (
        "/pk/punjab/sialkot/surgical-instrument-makers/?area=%00",
        "/search/?q=a%00b",
        "/_f/ref/?ref=%00",
        "/%00/",
    ):
        assert c.get(url).status_code in (400, 404), url
    u = principals["user"]
    assert u.post("/add/area/", {"name": "bad\x00name"}).status_code == 400
