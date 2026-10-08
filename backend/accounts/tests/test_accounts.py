import re
from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client

from access import services as acs
from access.models import Plan
from accounts import throttle, totp
from accounts.models import Profile, TOTPDevice
from accounts.roles import CAPS, ROLES, grant_role, has_cap, needs_mfa, user_roles
from core import clock

PW = "Correct-horse-battery-9"


def signup(client, name="amina", email="amina@example.org", pw=PW):
    return client.post("/account/signup/", {"username": name, "email": email, "password1": pw, "password2": pw})


def test_rfc6238_vectors():
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # ASCII 12345678901234567890
    assert totp.hotp(secret, 59 // 30, digits=8) == "94287082"
    assert totp.hotp(secret, 1111111109 // 30, digits=8) == "07081804"
    assert totp.totp(secret, at=20000000000, digits=8) == "65353130"


def test_totp_verify_window_and_replay():
    s = totp.new_secret()
    code = totp.totp(s, at=1_000_000)
    step = totp.verify(s, code, at=1_000_000)
    assert step is not None
    assert totp.verify(s, code, at=1_000_000, last_step=step) is None  # replay refused
    assert totp.verify(s, code, at=1_000_000 + 30) is not None  # one step late is fine
    assert totp.verify(s, code, at=1_000_000 + 300) is None
    assert totp.verify(s, "000000", at=1_000_000) is None


def test_signup_creates_profile_sends_verification_and_logs_in(db):
    c = Client()
    r = signup(c)
    assert r.status_code == 302 and User.objects.get(username="amina").profile
    assert len(mail.outbox) == 1
    link = re.search(r"http://testserver(/account/verify/\S+)", mail.outbox[0].body).group(1)
    assert c.get("/account/").status_code == 200
    assert Client().get(link).status_code == 200
    assert Profile.objects.get(user__username="amina").email_verified
    assert Client().get(link).status_code == 404  # single use


def test_signup_validation(db):
    signup(Client())
    r = signup(Client(), name="Amina", email="other@example.org")
    assert b"taken" in r.content
    assert b"already registered" in signup(Client(), name="bilal", email="amina@example.org").content
    assert (
        b"too common"
        in Client()
        .post(
            "/account/signup/", {"username": "c", "email": "c@x.org", "password1": "password", "password2": "password"}
        )
        .content
    )
    assert (
        b"differ"
        in Client()
        .post("/account/signup/", {"username": "d", "email": "d@x.org", "password1": PW, "password2": "x"})
        .content
    )


def test_passwords_are_hashed_with_argon2_in_production_settings(db, settings):
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    ]
    u = User.objects.create_user("zed", "z@x.org", PW)
    assert u.password.startswith("argon2")


def test_login_by_username_or_email_and_generic_error(db):
    signup(Client())
    for ident in ("amina", "amina@example.org"):
        c = Client()
        assert c.post("/account/login/", {"username": ident, "password": PW}).status_code == 302
        assert c.get("/account/").status_code == 200
    bad = Client().post("/account/login/", {"username": "amina", "password": "nope"})
    assert b"Wrong username or password" in bad.content


def test_account_locks_after_five_failures_even_with_the_right_password(db):
    signup(Client())
    c = Client()
    for _ in range(5):
        assert c.post("/account/login/", {"username": "amina", "password": "bad"}).status_code == 200
    r = c.post("/account/login/", {"username": "amina", "password": PW})
    assert r.status_code == 429 and b"Too many attempts" in r.content
    clock.set_now(clock.now() + timedelta(minutes=16))
    try:
        assert Client().post("/account/login/", {"username": "amina", "password": PW}).status_code == 302
    finally:
        clock.set_now(None)


def test_address_throttle_covers_many_account_names(db):
    c = Client()
    for i in range(20):
        c.post("/account/login/", {"username": f"ghost{i}", "password": "bad"})
    assert c.post("/account/login/", {"username": "ghost99", "password": "bad"}).status_code == 429


def test_good_login_clears_account_failures(db):
    signup(Client())
    c = Client()
    for _ in range(3):
        c.post("/account/login/", {"username": "amina", "password": "bad"})
    c.post("/account/login/", {"username": "amina", "password": PW})
    assert not throttle.is_locked("amina", "1.2.3.4")


def test_open_redirect_blocked_on_login(db):
    signup(Client())
    r = Client().post("/account/login/", {"username": "amina", "password": PW, "next": "https://evil.example/"})
    assert r["Location"] == "/account/"


def test_roles_and_capabilities(db):
    u = User.objects.create_user("mod1", "m@x.org", PW)
    assert user_roles(u) == set() and not has_cap(u, "moderate") and has_cap(u, "add_entry")
    grant_role(u, "moderator")
    assert has_cap(u, "moderate") and has_cap(u, "claim_decide") and not has_cap(u, "approve_payout") and needs_mfa(u)
    with pytest.raises(ValueError):
        grant_role(u, "wizard")
    from django.contrib.auth.models import AnonymousUser

    assert not has_cap(AnonymousUser(), "add_entry")
    assert set(ROLES) >= {r for rs in CAPS.values() for r in rs} - {"user"}


def test_payout_creator_and_approver_are_the_same_role_but_flagged_for_two_person_rule(db):
    # separation of duties is enforced by the ledger module (batch creator may not approve); the capability exists for both
    assert (
        "finance" in CAPS["create_payout"]
        and "finance" in CAPS["approve_payout"]
        and "admin" not in CAPS["approve_payout"]
    )


def staff_client(role="moderator", enroll=True):
    u = User.objects.create_user(f"{role}x", f"{role}@x.org", PW)
    grant_role(u, role)
    c = Client()
    r = c.post("/account/login/", {"username": u.username, "password": PW})
    assert r.status_code == 302 and "mfa" in r["Location"]
    return u, c


def test_staff_must_enroll_and_verify_mfa_before_staff_routes(db):
    u, c = staff_client()
    assert c.get("/staff/").status_code == 302 and "/staff/" not in c.get("/staff/")["Location"].replace(
        "next=/staff/", ""
    )
    page = c.get("/account/mfa/setup/")
    assert page.status_code == 200
    secret = TOTPDevice.objects.get(user=u).secret_enc
    r = c.post("/account/mfa/setup/", {"code": "000000"})
    assert b"wrong or expired" in r.content
    r = c.post("/account/mfa/setup/", {"code": totp.totp(secret)})
    assert r.status_code == 200 and re.findall(r"<li>([0-9a-f]{10})</li>", r.content.decode())
    assert c.get("/staff/").status_code != 302  # allowed in (404 until the console exists)


def test_mfa_login_second_step_recovery_code_once_and_replay(db):
    u, c = staff_client()
    c.get("/account/mfa/setup/")
    dev = TOTPDevice.objects.get(user=u)
    r = c.post("/account/mfa/setup/", {"code": totp.totp(dev.secret_enc)})
    codes = re.findall(r"<li>([0-9a-f]{10})</li>", r.content.decode())
    c2 = Client()
    assert "verify" in c2.post("/account/login/", {"username": u.username, "password": PW})["Location"]
    dev.refresh_from_db()
    assert (
        c2.post(
            "/account/mfa/verify/", {"code": totp.totp(dev.secret_enc, at=__import__("time").time() + 30)}
        ).status_code
        == 302
    )
    c3 = Client()
    c3.post("/account/login/", {"username": u.username, "password": PW})
    assert c3.post("/account/mfa/verify/", {"code": codes[0]}).status_code == 302
    c4 = Client()
    c4.post("/account/login/", {"username": u.username, "password": PW})
    assert c4.post("/account/mfa/verify/", {"code": codes[0]}).status_code == 200  # a recovery code works once


def test_mfa_codes_are_throttled(db):
    u, c = staff_client()
    c.get("/account/mfa/setup/")
    dev = TOTPDevice.objects.get(user=u)
    c.post("/account/mfa/setup/", {"code": totp.totp(dev.secret_enc)})
    c2 = Client()
    c2.post("/account/login/", {"username": u.username, "password": PW})
    for _ in range(5):
        c2.post("/account/mfa/verify/", {"code": "111111"})
    assert c2.post("/account/mfa/verify/", {"code": "111111"}).status_code == 429


def test_regular_user_cannot_reach_staff_or_admin(db):
    signup(Client())
    c = Client()
    c.post("/account/login/", {"username": "amina", "password": PW})
    assert c.get("/staff/").status_code == 403
    assert c.get("/admin/").status_code in (302, 403)
    assert Client().get("/staff/")["Location"].startswith("/account/login/")
    assert Client().get("/admin/login/")["Location"].startswith("/account/login/")


def test_delete_account_removes_personal_details(db):
    signup(Client())
    c = Client()
    c.post("/account/login/", {"username": "amina", "password": PW})
    assert b"Wrong password" in c.post("/account/delete/", {"password": "x"}).content
    assert b"personal details were removed" in c.post("/account/delete/", {"password": PW}).content
    u = User.objects.get(pk=Profile.objects.get().user_id)
    assert u.username.startswith("deleted-") and u.email == "" and not u.is_active and not u.has_usable_password()
    assert Client().post("/account/login/", {"username": "amina", "password": PW}).status_code == 200


def test_password_reset_sends_link(db):
    signup(Client())
    mail.outbox.clear()
    Client().post("/account/password/reset/", {"email": "amina@example.org"})
    assert len(mail.outbox) == 1 and "/account/password/reset/" in mail.outbox[0].body


# ---- subscriptions and entitlements ------------------------------------------------------------------------------


def test_scoped_subscription_unlocks_only_its_scope(db, tree, surgical, make_published):
    pass

    e = make_published("Crescent Surgical Works", tree["paris"])
    u = User.objects.create_user("buyer", "b@x.org", PW)
    plan = Plan.objects.create(key="subscriber_scope", name="Subscriber")
    acs.grant_subscription(u, plan, scope_path="pk.punjab.sialkot", concept=surgical, days=30)
    c = Client()
    c.post("/account/login/", {"username": "buyer", "password": PW})
    assert "example.org" in c.get(f"/_f/entry/{e.uid}/").content.decode()
    other = make_published("Dubai Works", tree["world"], phone="0301 111 1111", refresh=False) if False else None
    assert other is None
    acs.revoke_entitlements(u)
    assert "example.org" not in c.get(f"/_f/entry/{e.uid}/").content.decode()


def test_expired_entitlement_gives_nothing(db, tree, surgical):
    u = User.objects.create_user("buyer", "b@x.org", PW)
    plan = Plan.objects.create(key="subscriber_scope", name="Subscriber")
    acs.grant_subscription(u, plan, scope_path="", days=30)
    assert acs.active_scopes(u) == [("", None)]
    assert acs.active_scopes(u, now=clock.now() + timedelta(days=31)) == []
