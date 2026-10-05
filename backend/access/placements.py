"""Placements and ads (plan 9.4, rule R14). Platform revenue; neither touches the contributor pool, check labels or order."""

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Q

from core import clock
from core.models import audit
from entries.models import Entry
from places.models import Place

from .models import Ad, Placement

LEVELS = {1: "country", 2: "region", 3: "city", 4: "area"}  # place depth -> level name; world (0) cannot be sold


class PlacementError(ValueError):
    pass


def _under(path, base):
    return base == "" or path == base or path.startswith(base + ".")


def slots():
    return int(getattr(settings, "PLACEMENT_SLOTS", 2))


def level_of(place):
    if place.depth < 1:
        raise PlacementError("the whole world cannot be sponsored")
    return LEVELS.get(place.depth, "area")


def active_placements(place_path, concept_id, now=None):
    now = now or clock.now()
    return list(
        Placement.objects.filter(
            scope_path=place_path, concept_id=concept_id, state="active", starts_at__lte=now, ends_at__gt=now
        )
        .select_related("entry", "entry__place", "entry__primary_concept")
        .prefetch_related("entry__verification_current", "entry__namevariant_set", "entry__place__names")
        .order_by("slot")
    )


def signature(place_path, concept_id, now=None):
    """Goes into the page ETag so a new or expired placement changes the address the cache sees."""
    ps = active_placements(place_path, concept_id, now)
    return ",".join(f"{p.pk}.{int(p.updated_at.timestamp())}" for p in ps)


def any_sold(place_path=None):
    return Placement.objects.filter(state="active", ends_at__gt=clock.now()).exists()


def check_capacity(entry, place, concept, *, months=1, now=None):
    """Raise PlacementError when a placement could not be created now. Returns the free slot numbers."""
    now = now or clock.now()
    if entry.publish_state != Entry.PublishState.PUBLISHED or entry.status == Entry.Status.PERM_CLOSED:
        raise PlacementError("only a published, open entry can be sponsored")
    if not _under(entry.place_path, place.path):
        raise PlacementError("the entry is not in this place")
    from analytics.rollups import descendant_concept_ids

    if entry.primary_concept_id not in descendant_concept_ids(concept.pk):
        raise PlacementError("the entry is not on this list type")
    level_of(place)
    end = now + timedelta(days=30 * max(int(months), 1))
    overlapping = Placement.objects.filter(
        scope_path=place.path, concept=concept, state="active", starts_at__lt=end, ends_at__gt=now
    )
    if overlapping.filter(entry=entry).exists():
        raise PlacementError("this entry already has a placement on that list")
    used = set(overlapping.values_list("slot", flat=True))
    free = [s for s in range(1, slots() + 1) if s not in used]
    if not free:
        raise PlacementError("no free sponsored slot on this list for that period")
    return free


@transaction.atomic
def create_placement(entry, place, concept, *, months=1, price_minor=0, currency="USD", order_ref="", now=None):
    """A slot is free when fewer than PLACEMENT_SLOTS placements overlap the period. The entry must really be on the list
    it is sponsored on, be published and not closed; a check cannot be bought, so an unchecked entry shows 'Not verified yet'.
    """
    now = now or clock.now()
    Place.objects.select_for_update().filter(pk=place.pk).first()  # one sale at a time per place
    free = check_capacity(entry, place, concept, months=months, now=now)
    level = level_of(place)
    end = now + timedelta(days=30 * max(int(months), 1))
    p = Placement.objects.create(
        entry=entry,
        scope_path=place.path,
        concept=concept,
        level=level,
        slot=free[0],
        price_minor=price_minor,
        currency=currency,
        starts_at=now,
        ends_at=end,
        order_ref=order_ref,
    )
    audit(
        "placement.create", object_type="placement", object_uid=str(p.pk), payload={"entry": entry.uid, "slot": p.slot}
    )
    return p


def expire_due(now=None):
    now = now or clock.now()
    n = Placement.objects.filter(state="active", ends_at__lte=now).update(state="ended")
    m = Ad.objects.filter(state="active", ends_at__lte=now).update(state="ended")
    return n + m


# ---- ads ------------------------------------------------------------------------------------------------------------


@transaction.atomic
def submit_ad(user, entry, headline, body="", *, scope_path="", concept=None, months=1, order_ref="", now=None):
    """Only the owner of a published entry may advertise it. Text only; staff approve before it shows."""
    from entries.services import is_owner

    now = now or clock.now()
    if not is_owner(entry, user):
        raise PlacementError("only the owner of the entry can advertise it")
    headline, body = headline.strip(), body.strip()
    if not headline or len(headline) > 80 or len(body) > 160:
        raise PlacementError("headline up to 80 characters, text up to 160")
    from outreach.services import contact_leaks

    if contact_leaks(headline + " " + body):
        raise PlacementError("an ad cannot carry phone numbers, emails or links; it points to the entry page")
    return Ad.objects.create(
        advertiser=user,
        entry=entry,
        scope_path=scope_path,
        concept=concept,
        headline=headline,
        body=body,
        starts_at=now,
        ends_at=now + timedelta(days=30 * max(int(months), 1)),
        order_ref=order_ref,
    )


@transaction.atomic
def decide_ad(ad, *, actor, approve):
    if ad.state != Ad.State.PENDING:
        raise PlacementError("already decided")
    ad.state = Ad.State.ACTIVE if approve else Ad.State.REJECTED
    ad.save()
    audit("ad.decide", actor=actor, object_type="ad", object_uid=str(ad.pk), payload={"approved": approve})
    return ad


def pick_ad(place_path, concept_id, now=None):
    """The ad to show a free viewer: the most specific place match for the trade, then the least shown."""
    now = now or clock.now()
    cands = (
        Ad.objects.filter(state="active", starts_at__lte=now, ends_at__gt=now)
        .filter(Q(concept_id=concept_id) | Q(concept__isnull=True))
        .select_related("entry")
    )
    best = None
    for a in cands:
        if not _under(place_path, a.scope_path):
            continue
        key = (-len(a.scope_path), 0 if a.concept_id == concept_id else 1, a.shown)
        if best is None or key < best[0]:
            best = (key, a)
    return best[1] if best else None


def note_shown(ad):
    Ad.objects.filter(pk=ad.pk).update(shown=ad.shown + 1)
