"""Sign in with Google or ORCID (plan P6.02): the OAuth 2.0 authorisation-code flow with PKCE and a state check.
`http_post` and `http_get` are the only network calls and are replaced in tests."""

import base64
import hashlib
import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings

PROVIDERS = {
    "google": {
        "label": "Google",
        "authorize": "https://accounts.google.com/o/oauth2/v2/auth",
        "token": "https://oauth2.googleapis.com/token",
        "userinfo": "https://openidconnect.googleapis.com/v1/userinfo",
        "scope": "openid email profile",
    },
    "orcid": {
        "label": "ORCID",
        "authorize": "https://orcid.org/oauth/authorize",
        "token": "https://orcid.org/oauth/token",
        "userinfo": "",
        "scope": "/authenticate",
    },
}


class SocialError(ValueError):
    pass


def enabled(name):
    cfg = getattr(settings, "SOCIAL_PROVIDERS", {}).get(name)
    return bool(cfg and cfg.get("client_id") and cfg.get("client_secret") and name in PROVIDERS)


def enabled_providers():
    return [(n, PROVIDERS[n]["label"]) for n in PROVIDERS if enabled(n)]


def http_post(url, data):
    r = requests.post(url, data=data, headers={"Accept": "application/json"}, timeout=10)
    r.raise_for_status()
    return r.json()


def http_get(url, token):
    r = requests.get(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}, timeout=10)
    r.raise_for_status()
    return r.json()


def start(name, redirect_uri):
    """Returns (url to send the person to, session data to keep until the callback)."""
    if not enabled(name):
        raise SocialError("this sign-in is not available")
    cfg = settings.SOCIAL_PROVIDERS[name]
    state = secrets.token_urlsafe(24)
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    params = {
        "client_id": cfg["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": PROVIDERS[name]["scope"],
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return PROVIDERS[name]["authorize"] + "?" + urlencode(params), {
        "state": state,
        "verifier": verifier,
        "provider": name,
    }


def finish(name, code, saved, state, redirect_uri):
    """Exchange the code and return {"subject", "email", "email_verified", "name"}. Raises SocialError on any mismatch."""
    if not saved or saved.get("provider") != name or not state or not secrets.compare_digest(saved["state"], state):
        raise SocialError("the sign-in could not be confirmed; try again")
    if not enabled(name) or not code:
        raise SocialError("this sign-in is not available")
    cfg = settings.SOCIAL_PROVIDERS[name]
    try:
        tok = http_post(
            PROVIDERS[name]["token"],
            {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": cfg["client_id"],
                "client_secret": cfg["client_secret"],
                "code_verifier": saved["verifier"],
            },
        )
        if name == "orcid":
            if not tok.get("orcid"):
                raise SocialError("ORCID did not return an iD")
            return {"subject": tok["orcid"], "email": "", "email_verified": False, "name": tok.get("name", "")}
        info = http_get(PROVIDERS[name]["userinfo"], tok["access_token"])
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise SocialError("the provider did not accept the sign-in") from exc
    if not info.get("sub"):
        raise SocialError("the provider did not identify you")
    return {
        "subject": info["sub"],
        "email": (info.get("email") or "").lower(),
        "email_verified": bool(info.get("email_verified")),
        "name": info.get("name", ""),
    }
