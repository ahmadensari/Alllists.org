"""Levels, certificates, access credit and visible credit (plan P2.23). None of these is money (rule: rewards are
non-cash; money is paid only from sales). Safe to call after every completed task."""

import secrets
from datetime import timedelta

from django.db import transaction

from access.models import Entitlement
from core import clock
from core.models import audit

from .models import Reward  # noqa: F401  (re-exported for views)

ACCESS_CREDIT_FROM_LEVEL = 2
ACCESS_CREDIT_DAYS = 30


def _code():
    return secrets.token_hex(6).upper()


@transaction.atomic
def on_level_change(user, new_level, *, place_path=""):
    """Grant a certificate for each level reached once, and a month of access to the contributor's own city once they
    reach level 2. Returns the rewards made."""
    made = []
    for lvl in range(1, new_level + 1):
        detail = f"Level {lvl}"
        if not Reward.objects.filter(user=user, kind="certificate", detail=detail).exists():
            made.append(Reward.objects.create(user=user, kind="certificate", detail=detail, code=_code()))
    if new_level >= ACCESS_CREDIT_FROM_LEVEL and not Reward.objects.filter(user=user, kind="access_credit").exists():
        city = ".".join(place_path.split(".")[:3]) if place_path else ""
        now = clock.now()
        Entitlement.objects.create(
            user=user,
            kind=Entitlement.Kind.SUBSCRIPTION,
            scope_path=city,
            valid_from=now,
            valid_to=now + timedelta(days=ACCESS_CREDIT_DAYS),
            source="credit:level",
        )
        made.append(
            Reward.objects.create(
                user=user, kind="access_credit", detail=f"{ACCESS_CREDIT_DAYS} days, {city or 'world'}"
            )
        )
    for r in made:
        audit("reward.grant", object_type="user", object_uid=str(user.pk), payload={"kind": r.kind, "detail": r.detail})
    return made


def verify_certificate(code):
    """Public check of a certificate code: who (public name only) and what, or None."""
    r = Reward.objects.filter(kind="certificate", code=code.upper()).select_related("user").first()
    if r is None:
        return None
    prof = getattr(r.user, "contributor", None)
    from accounts.models import Profile

    name = ""
    if prof and prof.show_credit:
        name = getattr(Profile.objects.filter(user=r.user).first(), "display_name", "") or ""
    return {
        "name": name or "A contributor",
        "detail": r.detail,
        "date": r.granted_at.date().isoformat(),
        "code": r.code,
    }


def credit_line(entry):
    """The public 'Added by' name for an entry, or None. Only when the contributor opted in, the credit is eligible
    (a person checked it) and the entry is not an individual."""
    from accounts.models import Profile
    from entries.models import CreditEvent

    if entry.entity_type == "person":
        return None
    ev = (
        CreditEvent.objects.filter(entry=entry, kind="added", eligible=True, user__isnull=False)
        .order_by("created_at", "id")
        .first()
    )
    if ev is None:
        return None
    prof = getattr(ev.user, "contributor", None)
    if not (prof and prof.show_credit):
        return None
    name = getattr(Profile.objects.filter(user=ev.user).first(), "display_name", "")
    return name or None
