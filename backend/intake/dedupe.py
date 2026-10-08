"""Duplicate pipeline v1 (plan 7.4): block, score, decide. Scoped by place subtree and concept so it stays cheap."""

import math
from itertools import combinations

from core.textfold import fold
from entries.models import Contact, Entry

AUTO_MERGE = 0.90
REVIEW = 0.60
WEIGHTS = {"phone": 0.50, "name": 0.30, "distance": 0.10, "address": 0.10}


def trigrams(text):
    padded = f"  {text} "
    return {padded[i : i + 3] for i in range(len(padded) - 2)}


def similarity(a, b):
    """Jaccard similarity of trigrams of folded text, the same idea as pg_trgm."""
    ta, tb = trigrams(fold(a)), trigrams(fold(b))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(float(lat1)), math.radians(float(lat2))
    dphi, dl = p2 - p1, math.radians(float(lon2) - float(lon1))
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def features(a, b):
    kinds = ["phone", "mobile", "whatsapp"]
    phones_a = set(Contact.objects.filter(entry=a, kind__in=kinds).values_list("value_hash", flat=True))
    phones_b = set(Contact.objects.filter(entry=b, kind__in=kinds).values_list("value_hash", flat=True))
    f = {
        "phone": 1.0 if phones_a & phones_b else 0.0,
        "name": similarity(a.name, b.name),
        "address": similarity(a.address_text, b.address_text) if a.address_text and b.address_text else 0.0,
        "distance": 0.0,
    }
    if a.lat is not None and b.lat is not None:
        d = haversine_m(a.lat, a.lon, b.lat, b.lon)
        f["distance_m"] = round(d)
        f["distance"] = 1.0 if d <= 100 else 0.0
    return f


def score(f):
    s = sum(WEIGHTS[k] * f[k] for k in WEIGHTS)
    # a shared phone plus a similar name is as good as a match; an exact name alone never auto-merges
    if f["phone"] and f["name"] >= 0.5:
        s = max(s, 0.92)
    if f["distance"] and f["name"] >= 0.8:
        s = max(s, 0.92)  # same name within 100 m
    if f["name"] >= 0.8:
        # near-identical names inside one place and concept block always reach review, never auto-merge alone
        s = max(s, REVIEW + (f["name"] - 0.8) / 0.2 * 0.25)
    return round(min(s, 1.0), 4)


def candidates_for(entry):
    """Blocking: same country and concept, within the same place subtree, or sharing a phone hash."""
    base = Entry.objects.filter(
        country_code=entry.country_code, deleted_at__isnull=True, merged_into__isnull=True
    ).exclude(pk=entry.pk)
    same_place = base.filter(primary_concept=entry.primary_concept, place_path__startswith=entry.place_path)
    hashes = list(Contact.objects.filter(entry=entry).values_list("value_hash", flat=True))
    same_phone = base.filter(contact_set__value_hash__in=hashes) if hashes else base.none()
    seen, out = set(), []
    for e in list(same_place) + list(same_phone):
        if e.pk not in seen:
            seen.add(e.pk)
            out.append(e)
    return out


def scan_entry(entry):
    """Return [(other, score, features)] at or above the review threshold, best first."""
    found = []
    for other in candidates_for(entry):
        f = features(entry, other)
        s = score(f)
        if s >= REVIEW:
            found.append((other, s, f))
    return sorted(found, key=lambda t: -t[1])


def scan_all(country_code=None):
    """Batch scan of every pair inside each (place, concept) block. Returns the number of candidates stored."""
    from .models import DedupeCandidate

    qs = Entry.objects.filter(deleted_at__isnull=True, merged_into__isnull=True)
    if country_code:
        qs = qs.filter(country_code=country_code)
    blocks = {}
    for e in qs:
        blocks.setdefault((e.country_code, e.place_id, e.primary_concept_id), []).append(e)
    stored = 0
    for group in blocks.values():
        for a, b in combinations(sorted(group, key=lambda e: e.pk), 2):
            f = features(a, b)
            s = score(f)
            if s >= REVIEW:
                _, created = DedupeCandidate.objects.get_or_create(
                    a_entry=a, b_entry=b, defaults=dict(score=s, features=f)
                )
                stored += int(created)
    return stored
