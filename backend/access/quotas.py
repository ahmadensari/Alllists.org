"""Quotas and abuse counters (plan 9.3, P15). Counters live in the database so every worker sees the same numbers."""

from django.db import IntegrityError, transaction
from django.db.models import F

from core import clock
from core.clientip import client_address
from core.crypto import keyed_hash
from core.models import audit

from .models import QuotaCounter

FREE_NAMES_ACCOUNT = 100
FREE_NAMES_ANON = 40
FRAGMENT_ALARM = 500
FRAGMENT_HARD_CAP = 2000


def subject_for(request):
    """A keyed hash of the user id or the address, never the raw value."""
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        return keyed_hash(f"user:{user.pk}"), "account"
    addr = client_address(request)
    return keyed_hash(f"addr:{addr}"), "anon"


def hit(subject, key, amount=1):
    """Add to today's counter and return the new total."""
    day = clock.today()
    for _ in range(2):
        try:
            with transaction.atomic():
                row, created = QuotaCounter.objects.get_or_create(
                    subject=subject, key=key, day=day, defaults={"count": 0}
                )
                QuotaCounter.objects.filter(pk=row.pk).update(count=F("count") + amount)
                row.refresh_from_db()
                return row.count
        except IntegrityError:
            continue
    return QuotaCounter.objects.get(subject=subject, key=key, day=day).count


def current(subject, key):
    row = QuotaCounter.objects.filter(subject=subject, key=key, day=clock.today()).first()
    return row.count if row else 0


def free_name_limit(kind):
    return FREE_NAMES_ACCOUNT if kind == "account" else FREE_NAMES_ANON


def check_names(request, n_rows):
    """Count rows a free viewer is about to see. Returns (allowed, remaining, limit)."""
    subject, kind = subject_for(request)
    limit = free_name_limit(kind)
    used = current(subject, "names")
    if used + n_rows > limit:
        return False, max(limit - used, 0), limit
    hit(subject, "names", n_rows)
    return True, limit - used - n_rows, limit


def note_fragment(request):
    """One count per fragment request. Past the alarm line staff are told; past the hard cap the address is refused."""
    subject, kind = subject_for(request)
    total = hit(subject, "fragments")
    if total == FRAGMENT_ALARM:
        audit("abuse.alarm", object_type="subject", object_uid=subject[:16], payload={"fragments": total, "kind": kind})
    return total <= FRAGMENT_HARD_CAP
