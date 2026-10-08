"""Rules the mutation check found untested in sign-in, two-step sign-in, sign-up, throttling, social linking, the enquiry
limits and the fetcher's address checks."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, RequestFactory

from accounts import throttle, totp
from accounts.models import LoginAttempt, SocialIdentity, TOTPDevice
from entries import services as es
from outreach import services as relay

PW = "Correct-horse-battery-9"


def _mfa_user(name):
    u = User.objects.create_user(name, f"{name}@example.org", PW)
    dev = TOTPDevice.objects.create(user=u, secret_enc=totp.new_secret(), confirmed=True)
    return u, dev


# ---- two-step sign-in -------------------------------------------------------------------------------------------------------


def test_mfa_verify_without_a_device_goes_to_setup_not_an_error(db):
    u = User.objects.create_user("nodev", "n@x.org", PW)
    c = Client()
    s = c.session
    s["pre_mfa_user"] = u.pk
    s.save()
    r = c.get("/account/mfa/verify/")
    assert r.status_code == 302 and r["Location"] == "/account/mfa/setup/"
    TOTPDevice.objects.create(user=u, secret_enc=totp.new_secret(), confirmed=False)  # started but not confirmed
    assert c.get("/account/mfa/verify/")["Location"] == "/account/mfa/setup/"


def test_a_second_step_for_another_account_signs_in_that_account_not_the_old_one(db):
    a = User.objects.create_user("already_in", "a@x.org", PW)
    b, dev = _mfa_user("second_account")
    c = Client()
    c.force_login(a)
    s = c.session
    s["pre_mfa_user"] = b.pk
    s.save()
    r = c.post("/account/mfa/verify/", {"code": totp.totp(dev.secret_enc)})
    assert r.status_code == 302
    assert c.session["_auth_user_id"] == str(b.pk) and c.session["mfa_ok"] is True


def test_wrong_code_or_wrong_password_each_block_turning_two_step_off(db):
    u, dev = _mfa_user("disabler")
    c = Client()
    c.force_login(u)
    good = totp.totp(dev.secret_enc)
    c.post("/account/security/", {"action": "disable_mfa", "password": PW, "code": "000000"})
    assert TOTPDevice.objects.filter(pk=dev.pk).exists()  # right password, wrong code
    c.post("/account/security/", {"action": "disable_mfa", "password": "nope", "code": good})
    assert TOTPDevice.objects.filter(pk=dev.pk).exists()  # right code, wrong password
    c.post("/account/security/", {"action": "disable_mfa", "password": PW, "code": good})
    assert not TOTPDevice.objects.filter(pk=dev.pk).exists()


# ---- sign-up ----------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "username,ok", [("a" * 40, True), ("a" * 41, False), ("has@sign", False), ("", False), ("fine_name", True)]
)
def test_username_rules(db, username, ok):
    c = Client()
    r = c.post(
        "/account/signup/",
        {"username": username, "email": f"x{len(username)}@example.org", "password1": PW, "password2": PW},
    )
    assert (r.status_code == 302) is ok, (username, r.status_code)
    assert User.objects.filter(username=username).exists() is ok


# ---- login throttling ----------------------------------------------------------------------------------------------------------


def test_a_good_login_clears_the_failures_and_a_failure_count_locks(db):
    for _ in range(4):
        throttle.record("alice", "1.2.3.4", success=False)
    assert not throttle.is_locked("alice", "9.9.9.9")
    throttle.record("alice", "1.2.3.4", success=True)
    assert not LoginAttempt.objects.filter(kind="account", success=False).exists()  # the failures are gone
    for _ in range(5):
        throttle.record("alice", "1.2.3.4", success=False)
    assert throttle.is_locked("alice", "9.9.9.9")  # five failures lock the account from any address
    assert not throttle.is_locked("bob", "9.9.9.9")  # and only that account


def test_username_case_and_spaces_do_not_dodge_the_lock(db):
    for _ in range(5):
        throttle.record("Alice", "1.1.1.1", success=False)
    assert throttle.is_locked("  alice ", "8.8.8.8")


def test_client_address_prefers_the_edge_header_only_behind_cloudflare(settings):
    settings.BEHIND_CLOUDFLARE = True
    rf = RequestFactory()
    assert throttle.client_address(rf.get("/", HTTP_CF_CONNECTING_IP="5.5.5.5", REMOTE_ADDR="10.0.0.1")) == "5.5.5.5"
    assert throttle.client_address(rf.get("/", REMOTE_ADDR="10.0.0.1")) == "10.0.0.1"


# ---- social linking ------------------------------------------------------------------------------------------------------------


def test_a_link_started_by_one_account_cannot_attach_to_whoever_is_signed_in_at_the_callback(db, settings, monkeypatch):
    from accounts import social

    settings.SOCIAL_PROVIDERS = {"google": {"client_id": "g", "client_secret": "s"}}
    monkeypatch.setattr(social, "http_post", lambda url, data: {"access_token": "t"})
    monkeypatch.setattr(
        social, "http_get", lambda url, t: {"sub": "g-55", "email": "z@example.org", "email_verified": True}
    )
    a = User.objects.create_user("linker_a", "la@x.org", PW)
    b = User.objects.create_user("linker_b", "lb@x.org", PW)
    c = Client()
    c.force_login(a)
    r = c.get("/account/social/google/?link=1")
    from urllib.parse import parse_qs, urlparse

    state = parse_qs(urlparse(r["Location"]).query)["state"][0]
    c.logout()
    c.force_login(b)  # somebody else is signed in when the provider sends the browser back
    s = c.session
    s["social"] = {**{"state": state, "verifier": "v", "provider": "google"}, "link_user": a.pk, "next": "/account/"}
    s.save()
    c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert not SocialIdentity.objects.filter(user=b).exists()
    assert not SocialIdentity.objects.filter(user=a, subject="g-55").exists()  # a was not signed in either


# ---- enquiry limits ----------------------------------------------------------------------------------------------------------------


def _published(make_published, tree, n):
    return [
        make_published(f"Limit Works {i}", tree["paris"], phone=f"0300 000 {i:04d}", refresh=False) for i in range(n)
    ]


def test_message_length_and_reply_address_boundaries(entry, users):
    ok_text = "x" * relay.MAX_TEXT
    relay.send_enquiry(users["owner"], [entry], ok_text, "a@example.org")
    with pytest.raises(relay.RelayError):
        relay.send_enquiry(users["owner"], [entry], ok_text + "x", "a@example.org")
    local = "b" * (254 - len("@example.org"))
    relay.send_enquiry(users["owner"], [entry], "hello", local + "@example.org")  # exactly 254 characters is allowed
    with pytest.raises(relay.RelayError):
        relay.send_enquiry(users["owner"], [entry], "hello", "b" + local + "@example.org")
    for bad in ("a b@example.org", "a\tb@example.org", "a\x01b@example.org"):
        with pytest.raises(relay.RelayError):
            relay.send_enquiry(users["owner"], [entry], "hello", bad)


def test_fifty_recipients_is_the_most_and_twenty_enquiries_a_day_the_most(tree, surgical, make_published, users):
    entries = _published(make_published, tree, 51)
    with pytest.raises(relay.RelayError, match="at most 50"):
        relay.send_enquiry(users["owner"], entries, "hi", "a@example.org", allow_many=True)
    relay.send_enquiry(users["owner"], entries[:50], "hi", "a@example.org", allow_many=True)
    for _ in range(relay.MAX_ENQUIRIES_PER_DAY - 1):
        relay.send_enquiry(users["owner"], entries[:1], "hi", "a@example.org")
    with pytest.raises(relay.RelayError, match="daily limit"):
        relay.send_enquiry(users["owner"], entries[:1], "hi", "a@example.org")
    assert es


# ---- fetcher address checks ------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("url", ["https://user@public.example/", "https://:pw@public.example/"])
def test_a_url_with_only_a_user_or_only_a_password_is_refused(monkeypatch, url):
    import socket

    from agents import fetcher as fe

    monkeypatch.setattr(fe, "_real_getaddrinfo", lambda h, *a, **k: [(socket.AF_INET, 1, 6, "", ("93.184.216.34", 0))])
    with pytest.raises(fe.FetchRefused, match="credentials"):
        fe.check_url(url)


def test_fetcher_decodes_a_page_with_no_declared_charset(monkeypatch):
    import io
    import socket

    from agents import fetcher as fe

    monkeypatch.setattr(fe, "_real_getaddrinfo", lambda h, *a, **k: [(socket.AF_INET, 1, 6, "", ("93.184.216.34", 0))])
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)

    class Raw(io.BytesIO):
        def read(self, n=-1, decode_content=True):
            return super().read(n)

    class R:
        def __init__(self, status, body, enc=None):
            self.status_code, self.encoding, self.raw = status, enc, Raw(body)

    class H:
        def get(self, url, **kw):
            return R(200, b"User-agent: *\nAllow: /\n") if url.endswith("robots.txt") else R(200, "ڈاکٹر".encode())

    assert fe.HttpFetcher(http=H()).get("https://public.example/p").text == "ڈاکٹر"
