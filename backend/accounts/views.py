import hashlib
import secrets
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from core import clock
from core.models import audit

from . import throttle, totp
from . import social
from .models import EmailToken, Profile, RecoveryCode, SocialIdentity, TOTPDevice
from .roles import needs_mfa, user_roles

User = get_user_model()


def _ctx(request, **kw):
    kw.setdefault("title", "AllLists")
    kw.setdefault("robots", "noindex,follow")
    return kw


def _safe_next(request, default="/account/"):
    nxt = request.POST.get("next") or request.GET.get("next") or default
    ok = url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}, require_https=request.is_secure())
    return nxt if ok else default


def _hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def _send_verification(request, user):
    token = secrets.token_urlsafe(32)
    EmailToken.objects.create(
        user=user, token_hash=_hash(token), purpose="verify", expires_at=clock.now() + timedelta(days=3)
    )
    link = request.build_absolute_uri(f"/account/verify/{token}/")
    send_mail(
        "Confirm your AllLists email", f"Open this link to confirm your email address:\n{link}\n", None, [user.email]
    )


@require_http_methods(["GET", "POST"])
def signup(request):
    errors = []
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip().lower()
        p1, p2 = request.POST.get("password1", ""), request.POST.get("password2", "")
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError

        from access import quotas

        subject, _ = quotas.subject_for(request)
        if quotas.hit(subject, "signup") > 5:
            errors.append(("username", "Too many sign-ups from this connection today. Try again tomorrow."))
        elif not username or "@" in username or len(username) > 40:
            errors.append(("username", "Choose a username without @ (up to 40 characters)."))
        elif User.objects.filter(username__iexact=username).exists():
            errors.append(("username", "That username is taken."))
        if "@" not in email:
            errors.append(("email", "Enter a valid email address."))
        elif User.objects.filter(email__iexact=email).exists():
            errors.append(("email", "That email is already registered."))
        if p1 != p2:
            errors.append(("password2", "The two passwords differ."))
        else:
            try:
                validate_password(p1, user=User(username=username, email=email))
            except ValidationError as exc:
                errors += [("password1", m) for m in exc.messages]
        if not errors:
            with transaction.atomic():
                user = User.objects.create_user(username, email, p1)
                Profile.objects.create(user=user, lang=getattr(request, "lang", "en"))
                audit("account.signup", actor=user, object_type="user", object_uid=str(user.pk))
            _send_verification(request, user)
            login(request, user)
            return redirect("/account/")
    return render(request, "accounts/signup.html", _ctx(request, errors=errors, form=request.POST))


def verify_email(request, token):
    row = (
        EmailToken.objects.filter(
            token_hash=_hash(token), purpose="verify", used_at__isnull=True, expires_at__gt=clock.now()
        )
        .select_related("user")
        .first()
    )
    if row is None:
        raise Http404
    row.used_at = clock.now()
    row.save(update_fields=["used_at"])
    Profile.objects.filter(user=row.user).update(email_verified=True)
    return render(
        request,
        "accounts/message.html",
        _ctx(request, heading="Email confirmed", body="Thank you. Your email is confirmed."),
    )


@require_http_methods(["GET", "POST"])
def login_view(request):
    error = ""
    if request.method == "POST":
        name = (request.POST.get("username") or "").strip()
        addr = throttle.client_address(request)
        if throttle.is_locked(name, addr):
            error = "Too many attempts. Wait 15 minutes and try again."
            return render(
                request, "accounts/login.html", _ctx(request, error=error, next=_safe_next(request)), status=429
            )
        user = authenticate(request, username=name, password=request.POST.get("password", ""))
        if user is None and "@" in name:
            u = User.objects.filter(email__iexact=name).first()
            user = authenticate(request, username=u.username, password=request.POST.get("password", "")) if u else None
        throttle.record(name, addr, success=user is not None)
        if user is None:
            error = "Wrong username or password."
        elif needs_mfa(user):
            request.session["pre_mfa_user"] = user.pk
            request.session["pre_mfa_next"] = _safe_next(request)
            return redirect(
                "/account/mfa/verify/" if hasattr(user, "totp") and user.totp.confirmed else "/account/mfa/setup/"
            )
        else:
            login(request, user)
            audit("account.login", actor=user, object_type="user", object_uid=str(user.pk))
            return redirect(_safe_next(request))
    return render(
        request,
        "accounts/login.html",
        _ctx(request, error=error, next=_safe_next(request), providers=social.enabled_providers()),
    )


@require_POST
def logout_view(request):
    logout(request)
    return redirect("/")


def _pending_user(request):
    uid = request.session.get("pre_mfa_user")
    return (
        User.objects.filter(pk=uid, is_active=True).first()
        if uid
        else (request.user if request.user.is_authenticated else None)
    )


@require_http_methods(["GET", "POST"])
def mfa_setup(request):
    user = _pending_user(request)
    if user is None:
        return redirect("/account/login/")
    dev = getattr(user, "totp", None)
    if dev and dev.confirmed:
        return redirect("/account/mfa/verify/")
    if dev is None:
        dev = TOTPDevice.objects.create(user=user, secret_enc=totp.new_secret())
    secret = dev.secret_enc
    error, codes = "", None
    if request.method == "POST":
        step = totp.verify(secret, request.POST.get("code", ""), last_step=dev.last_step)
        if step is None:
            error = "That code is wrong or expired."
        else:
            dev.confirmed, dev.last_step = True, step
            dev.save()
            codes = [secrets.token_hex(5) for _ in range(8)]
            RecoveryCode.objects.filter(user=user).delete()
            RecoveryCode.objects.bulk_create([RecoveryCode(user=user, code_hash=_hash(c)) for c in codes])
            _finish_mfa(request, user)
            audit("account.mfa_enrolled", actor=user, object_type="user", object_uid=str(user.pk))
    return render(
        request,
        "accounts/mfa_setup.html",
        _ctx(request, secret=secret, uri=totp.provisioning_uri(secret, user.username), error=error, codes=codes),
    )


def _finish_mfa(request, user):
    nxt = request.session.pop("pre_mfa_next", "/account/")
    request.session.pop("pre_mfa_user", None)
    if not request.user.is_authenticated or request.user.pk != user.pk:
        login(request, user)
    request.session["mfa_ok"] = True
    request.session["mfa_next"] = nxt


@require_http_methods(["GET", "POST"])
def mfa_verify(request):
    user = _pending_user(request)
    if user is None:
        return redirect("/account/login/")
    dev = getattr(user, "totp", None)
    if not dev or not dev.confirmed:
        return redirect("/account/mfa/setup/")
    addr = throttle.client_address(request)
    error = ""
    if request.method == "POST":
        if throttle.is_locked(f"mfa:{user.username}", addr):
            return render(
                request,
                "accounts/mfa_verify.html",
                _ctx(request, error="Too many attempts. Wait 15 minutes."),
                status=429,
            )
        code = request.POST.get("code", "")
        step = totp.verify(dev.secret_enc, code, last_step=dev.last_step)
        ok = False
        if step is not None:
            dev.last_step = step
            dev.save(update_fields=["last_step"])
            ok = True
        else:
            rc = RecoveryCode.objects.filter(
                user=user, code_hash=_hash(code.strip().lower()), used_at__isnull=True
            ).first()
            if rc:
                rc.used_at = clock.now()
                rc.save(update_fields=["used_at"])
                ok = True
        throttle.record(f"mfa:{user.username}", addr, success=ok)
        if ok:
            _finish_mfa(request, user)
            audit("account.login_mfa", actor=user, object_type="user", object_uid=str(user.pk))
            return redirect(request.session.pop("mfa_next", "/account/"))
        error = "That code is wrong or expired."
    return render(request, "accounts/mfa_verify.html", _ctx(request, error=error))


@login_required(login_url="/account/login/")
def dashboard(request):
    return render(
        request,
        "accounts/dashboard.html",
        _ctx(request, roles=sorted(user_roles(request.user)), profile=getattr(request.user, "profile", None)),
    )


@login_required(login_url="/account/login/")
@require_http_methods(["GET", "POST"])
def delete_account(request):
    error = ""
    if request.method == "POST":
        if not request.user.check_password(request.POST.get("password", "")):
            error = "Wrong password."
        else:
            user = request.user
            audit("account.delete", actor=user, object_type="user", object_uid=str(user.pk))
            logout(request)
            with transaction.atomic():
                user.is_active = False
                user.username, user.email, user.first_name, user.last_name = f"deleted-{user.pk}", "", "", ""
                user.set_unusable_password()
                user.save()
                Profile.objects.filter(user=user).update(display_name="", saved_place_uid="")
                user.groups.clear()
                TOTPDevice.objects.filter(user=user).delete()
                RecoveryCode.objects.filter(user=user).delete()
            return render(
                request,
                "accounts/message.html",
                _ctx(request, heading="Account deleted", body="Your personal details were removed."),
            )
    return render(request, "accounts/delete.html", _ctx(request, error=error))


# ---- security page, optional two-step for everyone, and social sign-in (plan P6.02) -------------------------------------


@login_required(login_url="/account/login/")
@require_http_methods(["GET", "POST"])
def security(request):
    user = request.user
    dev = getattr(user, "totp", None)
    has_mfa = bool(dev and dev.confirmed)
    forced = bool(user_roles(user) & {"moderator", "finance", "admin", "surveyor_lead"}) or user.is_staff
    error = ""
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "enable_mfa" and not has_mfa:
            request.session["pre_mfa_next"] = "/account/security/"
            return redirect("/account/mfa/setup/")
        if action == "disable_mfa" and has_mfa:
            step = totp.verify(dev.secret_enc, request.POST.get("code", ""), last_step=dev.last_step)
            if forced:
                error = "Your role requires two-step sign-in; it cannot be turned off."
            elif not user.check_password(request.POST.get("password", "")) or step is None:
                error = "Enter your password and a current code to turn it off."
            else:
                dev.delete()
                RecoveryCode.objects.filter(user=user).delete()
                audit("account.mfa_disabled", actor=user, object_type="user", object_uid=str(user.pk))
                return redirect("/account/security/")
        if action == "unlink":
            ident = SocialIdentity.objects.filter(pk=request.POST.get("id") or 0, user=user).first()
            if ident and user.has_usable_password():
                ident.delete()
                audit("account.social_unlink", actor=user, object_type="user", object_uid=str(user.pk))
            else:
                error = "Set a password before removing your only way to sign in."
    return render(
        request,
        "accounts/security.html",
        _ctx(
            request,
            has_mfa=has_mfa,
            forced=forced,
            error=error,
            linked=list(SocialIdentity.objects.filter(user=user)),
            available=[
                (n, lbl)
                for n, lbl in social.enabled_providers()
                if not SocialIdentity.objects.filter(user=user, provider=n).exists()
            ],
        ),
    )


def _redirect_uri(request, name):
    return request.build_absolute_uri(f"/account/social/{name}/callback/")


def social_start(request, provider):
    if not social.enabled(provider):
        raise Http404
    url, saved = social.start(provider, _redirect_uri(request, provider))
    saved["link_user"] = request.user.pk if request.user.is_authenticated and request.GET.get("link") else None
    saved["next"] = _safe_next(request)
    request.session["social"] = saved
    return redirect(url)


def social_callback(request, provider):
    if not social.enabled(provider):
        raise Http404
    saved = request.session.pop("social", None)
    try:
        who = social.finish(
            provider, request.GET.get("code", ""), saved, request.GET.get("state", ""), _redirect_uri(request, provider)
        )
    except social.SocialError as exc:
        return render(
            request, "accounts/message.html", _ctx(request, heading="Sign-in failed", body=str(exc)), status=400
        )
    ident = SocialIdentity.objects.filter(provider=provider, subject=who["subject"]).select_related("user").first()
    if saved.get("link_user") and request.user.is_authenticated and request.user.pk == saved["link_user"]:
        if ident and ident.user_id != request.user.pk:
            return render(
                request,
                "accounts/message.html",
                _ctx(request, heading="Already linked", body="That account is linked to another AllLists account."),
                status=409,
            )
        SocialIdentity.objects.get_or_create(user=request.user, provider=provider, subject=who["subject"])
        audit(
            "account.social_link",
            actor=request.user,
            object_type="user",
            object_uid=str(request.user.pk),
            payload={"provider": provider},
        )
        return redirect("/account/security/")
    if ident is None:
        user = _social_user(request, provider, who)
        if user is None:
            return render(
                request,
                "accounts/message.html",
                _ctx(
                    request,
                    heading="Use your password first",
                    body=(
                        "An account with this email already exists and its email is not confirmed here. "
                        "Sign in with your password, then link this provider from Security."
                    ),
                ),
                status=409,
            )
    else:
        user = ident.user
    if not user.is_active:
        raise Http404
    if needs_mfa(user):
        request.session["pre_mfa_user"] = user.pk
        request.session["pre_mfa_next"] = saved.get("next", "/account/")
        return redirect(
            "/account/mfa/verify/" if hasattr(user, "totp") and user.totp.confirmed else "/account/mfa/setup/"
        )
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    audit(
        "account.login_social", actor=user, object_type="user", object_uid=str(user.pk), payload={"provider": provider}
    )
    return redirect(saved.get("next", "/account/"))


@transaction.atomic
def _social_user(request, provider, who):
    """Find or make the account for a first-time provider sign-in. Never takes over an account by an unconfirmed email."""
    existing = User.objects.filter(email__iexact=who["email"]).first() if who["email"] else None
    if existing is not None:
        confirmed = Profile.objects.filter(user=existing, email_verified=True).exists()
        if not (confirmed and who["email_verified"]):
            return None
        user = existing
    else:
        base = f"{provider[:1]}-{who['subject'].replace('-', '')[-10:]}".lower()
        username, n = base, 1
        while User.objects.filter(username__iexact=username).exists():
            n += 1
            username = f"{base}{n}"
        user = User.objects.create_user(username, who["email"] if who["email_verified"] else "")
        user.set_unusable_password()
        user.save(update_fields=["password"])
        Profile.objects.create(
            user=user,
            lang=getattr(request, "lang", "en"),
            email_verified=bool(who["email_verified"]),
            display_name=who["name"][:60],
        )
        audit("account.signup", actor=user, object_type="user", object_uid=str(user.pk), payload={"provider": provider})
    SocialIdentity.objects.create(user=user, provider=provider, subject=who["subject"])
    return user
