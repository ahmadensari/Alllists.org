"""Login throttling (plan 11.1). The first build answered 20 wrong passwords in a row; this refuses them."""

from datetime import timedelta

from django.conf import settings

from core import clock
from core.clientip import client_address as _client_address
from core.crypto import keyed_hash

from .models import LoginAttempt

WINDOW = timedelta(minutes=15)


def _limits():
    return getattr(settings, "LOGIN_MAX_PER_ACCOUNT", 5), getattr(settings, "LOGIN_MAX_PER_ADDRESS", 20)


def _hash(kind, value):
    return keyed_hash(f"{kind}:{(value or '').strip().lower()}")


def is_locked(username, address):
    per_account, per_address = _limits()
    since = clock.now() - WINDOW
    a = LoginAttempt.objects.filter(key_hash=_hash("account", username), kind="account", success=False, ts__gte=since)
    b = LoginAttempt.objects.filter(key_hash=_hash("address", address), kind="address", success=False, ts__gte=since)
    return a.count() >= per_account or b.count() >= per_address


def record(username, address, success):
    LoginAttempt.objects.create(key_hash=_hash("account", username), kind="account", success=success)
    LoginAttempt.objects.create(key_hash=_hash("address", address), kind="address", success=success)
    if success:  # a good login clears the account's recent failures
        LoginAttempt.objects.filter(key_hash=_hash("account", username), kind="account", success=False).delete()


def client_address(request):
    return _client_address(request)
