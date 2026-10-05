import pytest
from django.contrib.auth.models import User
from django.test import Client
from urllib.parse import parse_qs, urlparse

from accounts import social, totp
from accounts.models import Profile, RecoveryCode, SocialIdentity, TOTPDevice
from accounts.roles import grant_role, needs_mfa

PW = "Correct-horse-battery-9"


@pytest.fixture
def providers(settings):
    settings.SOCIAL_PROVIDERS = {
        "google": {"client_id": "gid", "client_secret": "gsecret"},
        "orcid": {"client_id": "oid", "client_secret": "osecret"},
    }


def _fake(monkeypatch, info=None, orcid=None):
    calls = {}

    def post(url, data):
        calls["post"] = (url, data)
        if "orcid" in url:
            return {"access_token": "t", "orcid": orcid or "0000-0002-1825-0097", "name": "J Carberry"}
        return {"access_token": "tok"}

    def get(url, token):
        calls["get"] = (url, token)
        return info or {"sub": "g-123", "email": "new@example.org", "email_verified": True, "name": "New Person"}

    monkeypatch.setattr(social, "http_post", post)
    monkeypatch.setattr(social, "http_get", get)
    return calls


def _go(c, provider="google", extra=""):
    r = c.get(f"/account/social/{provider}/{extra}")
    assert r.status_code == 302
    q = parse_qs(urlparse(r["Location"]).query)
    return q["state"][0], q


def test_provider_is_off_without_keys(db, settings):
    settings.SOCIAL_PROVIDERS = {}
    assert Client().get("/account/social/google/").status_code == 404
    assert "Google" not in Client().get("/account/login/").content.decode()


def test_google_sign_in_creates_a_confirmed_account_and_uses_pkce(db, providers, monkeypatch):
    calls = _fake(monkeypatch)
    c = Client()
    state, q = _go(c)
    assert q["code_challenge_method"] == ["S256"] and q["client_id"] == ["gid"]
    r = c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert r.status_code == 302 and calls["post"][1]["code_verifier"]
    u = User.objects.get(email="new@example.org")
    assert not u.has_usable_password() and Profile.objects.get(user=u).email_verified
    assert SocialIdentity.objects.filter(user=u, provider="google", subject="g-123").exists()
    assert c.get("/account/").status_code == 200
    # a second sign-in finds the same account
    c2 = Client()
    state, _ = _go(c2)
    c2.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert User.objects.count() == 1


def test_wrong_state_or_missing_session_is_refused(db, providers, monkeypatch):
    _fake(monkeypatch)
    c = Client()
    _go(c)
    assert c.get("/account/social/google/callback/", {"code": "abc", "state": "forged"}).status_code == 400
    assert Client().get("/account/social/google/callback/", {"code": "abc", "state": "x"}).status_code == 400
    assert User.objects.count() == 0


def test_existing_unconfirmed_email_is_never_taken_over(db, providers, monkeypatch):
    User.objects.create_user("victim", "new@example.org", PW)
    Profile.objects.create(user=User.objects.get(username="victim"), email_verified=False)
    _fake(monkeypatch)
    c = Client()
    state, _ = _go(c)
    r = c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert r.status_code == 409 and not SocialIdentity.objects.exists()
    assert c.get("/account/").status_code == 302  # not signed in


def test_confirmed_account_is_linked_by_verified_email(db, providers, monkeypatch):
    u = User.objects.create_user("known", "new@example.org", PW)
    Profile.objects.create(user=u, email_verified=True)
    _fake(monkeypatch)
    c = Client()
    state, _ = _go(c)
    c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert SocialIdentity.objects.get().user_id == u.pk and User.objects.count() == 1


def test_orcid_sign_in_needs_no_email(db, providers, monkeypatch):
    _fake(monkeypatch)
    c = Client()
    state, _ = _go(c, "orcid")
    c.get("/account/social/orcid/callback/", {"code": "abc", "state": state})
    ident = SocialIdentity.objects.get(provider="orcid")
    assert ident.subject == "0000-0002-1825-0097" and ident.user.email == ""


def test_linking_and_unlinking_from_security_page(db, providers, monkeypatch):
    u = User.objects.create_user("linker", "l@example.org", PW)
    _fake(monkeypatch, info={"sub": "g-777", "email": "other@example.org", "email_verified": True})
    c = Client()
    c.force_login(u)
    assert "Link Google" in c.get("/account/security/").content.decode()
    state, _ = _go(c, extra="?link=1")
    c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    ident = SocialIdentity.objects.get(user=u)
    c.post("/account/security/", {"action": "unlink", "id": ident.pk})
    assert not SocialIdentity.objects.exists()


def test_social_only_user_cannot_unlink_their_only_sign_in(db, providers, monkeypatch):
    _fake(monkeypatch)
    c = Client()
    state, _ = _go(c)
    c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    ident = SocialIdentity.objects.get()
    c.post("/account/security/", {"action": "unlink", "id": ident.pk})
    assert SocialIdentity.objects.exists()


def test_staff_role_still_needs_the_second_step_after_social_sign_in(db, providers, monkeypatch):
    u = User.objects.create_user("modsocial", "new@example.org", PW)
    Profile.objects.create(user=u, email_verified=True)
    grant_role(u, "moderator")
    _fake(monkeypatch)
    c = Client()
    state, _ = _go(c)
    r = c.get("/account/social/google/callback/", {"code": "abc", "state": state})
    assert r.status_code == 302 and "/account/mfa/" in r["Location"]
    assert c.get("/staff/").status_code == 302


# ---- optional two-step for everyone ---------------------------------------------------------------------------------------


def _enrol(c, user):
    c.force_login(user)
    r = c.post("/account/security/", {"action": "enable_mfa"})
    assert r["Location"] == "/account/mfa/setup/"
    page = c.get("/account/mfa/setup/")
    secret = TOTPDevice.objects.get(user=user).secret_enc
    code = totp.totp(secret)
    return secret, code, page


def test_ordinary_user_can_turn_two_step_on_and_login_then_asks_for_it(db):
    u = User.objects.create_user("plain", "p@example.org", PW)
    assert not needs_mfa(u)
    c = Client()
    secret, code, _ = _enrol(c, u)
    c.post("/account/mfa/setup/", {"code": code})
    u.refresh_from_db()
    assert u.totp.confirmed and needs_mfa(u) and RecoveryCode.objects.filter(user=u).count() == 8
    fresh = Client()
    r = fresh.post("/account/login/", {"username": "plain", "password": PW})
    assert r["Location"] == "/account/mfa/verify/"
    assert fresh.get("/account/").status_code == 302  # password alone is not enough any more


def test_turning_it_off_needs_password_and_code_and_staff_cannot(db):
    u = User.objects.create_user("plain2", "p2@example.org", PW)
    dev = TOTPDevice.objects.create(user=u, secret_enc=totp.new_secret(), confirmed=True)
    c = Client()
    c.force_login(u)
    c.post("/account/security/", {"action": "disable_mfa", "password": "wrong", "code": "000000"})
    assert TOTPDevice.objects.filter(pk=dev.pk).exists()
    code = totp.totp(dev.secret_enc)
    c.post("/account/security/", {"action": "disable_mfa", "password": PW, "code": code})
    assert not TOTPDevice.objects.filter(pk=dev.pk).exists()
    staff = User.objects.create_user("staff1", "s@example.org", PW)
    grant_role(staff, "finance")
    TOTPDevice.objects.create(user=staff, secret_enc=totp.new_secret(), confirmed=True)
    sc = Client()
    sc.force_login(staff)
    assert "requires it" in sc.get("/account/security/").content.decode()
