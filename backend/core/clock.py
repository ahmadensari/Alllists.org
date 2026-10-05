"""One clock so tests can set the time."""
from django.utils import timezone

_override = None


def now():
    return _override or timezone.now()


def set_now(value):
    global _override
    _override = value


def today():
    return now().date()
