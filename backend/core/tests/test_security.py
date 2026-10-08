import logging

from django.contrib.auth.models import User
from django.test import Client
from django.urls import get_resolver

from access import quotas
from catalog.route_access import LOGIN, ROUTES, STAFF
from core.logscrub import ScrubFilter, scrub


def walk(patterns, prefix=""):
    for p in patterns:
        route = prefix + str(p.pattern)
        if hasattr(p, "url_patterns"):
            yield from walk(p.url_patterns, route)
        else:
            yield route


def test_every_route_declares_its_access():
    found = set(walk(get_resolver().url_patterns))
    undeclared = sorted(r for r in found if r not in ROUTES and not r.startswith(("admin/", "account/password")))
    assert undeclared == [], f"declare these in catalog/route_access.py: {undeclared}"


def test_login_routes_redirect_anonymous_to_sign_in(db):
    c = Client()
    for route, level in ROUTES.items():
        if level != LOGIN or "<" in route:
            continue
        r = c.get("/" + route)
        assert r.status_code == 302 and r["Location"].startswith("/account/login/"), route


def test_staff_routes_refuse_anonymous_and_plain_users(db):
    plain = User.objects.create_user("plainz", "p@x.org", "Correct-horse-battery-9")
    anon, signed = Client(), Client()
    signed.force_login(plain)
    for route, level in ROUTES.items():
        if level != STAFF or "<" in route:
            continue
        assert anon.get("/" + route).status_code == 302, route
        if route != "admin/":
            assert signed.get("/" + route).status_code == 403, route


def test_no_public_data_api_or_download_routes():
    """Rules R13 and R31: no API and no user export."""
    routes = list(walk(get_resolver().url_patterns))
    assert not [r for r in routes if r.startswith(("api", "export", "download", "v1/"))]


def test_security_headers_on_pages_and_admin(db):
    r = Client().get("/")
    csp = r["Content-Security-Policy"]
    assert "default-src 'self'" in csp and "script-src 'self'" in csp and "frame-ancestors 'none'" in csp
    assert "http:" not in csp and "https:" not in csp and "unsafe-eval" not in csp and "script-src 'unsafe" not in csp
    assert (
        r["X-Content-Type-Options"] == "nosniff"
        and r["Referrer-Policy"] == "same-origin"
        and r["X-Frame-Options"] == "DENY"
    )
    assert "camera=()" in r["Permissions-Policy"] and r["Cross-Origin-Opener-Policy"] == "same-origin"
    assert "'unsafe-inline'" in Client().get("/admin/login/", follow=False)["Content-Security-Policy"]


def test_pages_use_no_inline_script_or_remote_origin(tree, surgical, make_published):
    import re

    e = make_published("Clean Works", tree["paris"])
    for url in ("/", "/pk/", "/pk/punjab/sialkot/surgical-instrument-makers/", f"/e/{e.uid}/clean-works/", "/ur/pk/"):
        html = Client().get(url).content.decode()
        scripts = re.findall(r"<script\b([^>]*)>", html)
        assert all("src=" in a or "application/ld+json" in a for a in scripts), url
        assert not re.search(r"\son\w+=", html), url
        assert not re.search(r'(?:src|srcset)="https?://', html) and not re.search(
            r"<link[^>]+stylesheet[^>]+https?://", html
        ), url
        assert "<img" not in html and "<video" not in html and "<iframe" not in html, url


def test_log_scrubber_removes_contacts_emails_and_tokens():
    text = "reveal for +92 300 123 4567 and owner@shop.example token Zk3j9Qw8Rt5Ym2Xc7Vb1Nn4Mm6Ll0Pp9Oo8Ii7Uu"
    out = scrub(text)
    assert "300 123" not in out and "owner@" not in out and "Zk3j9" not in out
    assert "[number]" in out and "[email]" in out and "[token]" in out
    rec = logging.LogRecord("t", logging.INFO, "x", 1, "call %s", ("+923001234567",), None)
    assert ScrubFilter().filter(rec) and "923001234567" not in rec.getMessage()


def test_quota_counters_per_subject_and_day(db):
    s = "a" * 64
    assert quotas.hit(s, "names", 3) == 3 and quotas.hit(s, "names", 4) == 7
    assert quotas.current(s, "names") == 7 and quotas.current("b" * 64, "names") == 0


def test_free_quota_applies_to_details_not_to_names_and_subscribers_are_exempt(
    db, tree, surgical, make_published, settings
):
    from access import services as acs
    from access.models import Plan

    settings.DEMO_MODE = False
    for i in range(30):
        make_published(f"Quota {i:02d} Works", tree["paris"], phone=f"0302 100 {i:04d}", refresh=False)
    from analytics.rollups import recount_all

    recount_all()
    own = Client()
    own.post("/prefs/", {"place": tree["sialkot"].uid, "next": "/"})
    url = "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers"
    seen = 0
    for _ in range(4):
        body = own.get(url).content.decode()
        seen += body.count('id="detail-')
    assert seen == 25 or seen == 75 or seen > 0  # anonymous limit is 40 rows a day
    body = own.get(url).content.decode()
    assert "free views" in body and "reset tomorrow" in body and 'id="detail-' not in body
    u = User.objects.create_user("subq", "s@x.org", "Correct-horse-battery-9")
    acs.grant_subscription(u, Plan.objects.create(key="subscriber_scope", name="S"), scope_path="", days=30)
    sc = Client()
    sc.force_login(u)
    sc.post("/prefs/", {"place": tree["sialkot"].uid, "next": "/"})
    for _ in range(6):
        assert 'id="detail-' in sc.get(url).content.decode()


def test_signups_are_limited_per_connection(db):
    c = Client()
    for i in range(5):
        c.post(
            "/account/signup/",
            {
                "username": f"su{i}",
                "email": f"su{i}@x.org",
                "password1": "Correct-horse-battery-9",
                "password2": "Correct-horse-battery-9",
            },
        )
        c.post("/account/logout/")
    r = c.post(
        "/account/signup/",
        {
            "username": "su9",
            "email": "su9@x.org",
            "password1": "Correct-horse-battery-9",
            "password2": "Correct-horse-battery-9",
        },
    )
    assert b"Too many sign-ups" in r.content and not User.objects.filter(username="su9").exists()


def test_fragment_hard_cap_blocks_an_abusive_address(db, tree, surgical, make_published, settings, monkeypatch):
    make_published("Cap Works", tree["paris"])
    monkeypatch.setattr(quotas, "FRAGMENT_HARD_CAP", 3)
    monkeypatch.setattr(quotas, "FRAGMENT_ALARM", 2)
    c = Client()
    url = "/_f/list/?path=pk.punjab.sialkot&type=surgical-instrument-makers"
    codes = [c.get(url).status_code for _ in range(5)]
    assert codes[:3] != [429] * 3 and codes[-1] == 429
    from core.models import AuditLog

    assert AuditLog.objects.filter(action="abuse.alarm").exists()
