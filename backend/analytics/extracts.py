"""Statistics reports and custom extracts (plan 9.5, rules R13 and R30).

Statistics are aggregates only; small cells are hidden so no single business is identifiable. The extract is the one
way list data leaves the platform: staff run it for a paying buyer, contact values are never included, and a few
made-up businesses unique to that extract are planted so a leak can be traced."""

import csv
import hashlib
import io
import math
import secrets
from pathlib import Path

from django.conf import settings
from django.db import transaction

from catalog.queries import best_level, published_entries
from core import clock
from core.models import audit
from entries.models import Entry
from taxonomy.models import Concept

from .models import Extract, RollupCell, TraceEntry

MIN_CELL = 5  # a count below this is shown as "fewer than 5"
COLUMNS = ["code", "name", "other_name", "list_type", "place", "address", "website", "status", "check", "checked_on"]

_ADJ = ["Crescent", "Meridian", "Summit", "Harbor", "Pioneer", "Orchid", "Granite", "Lantern", "Cedar", "Falcon"]
_NOUN = ["Traders", "Works", "Industries", "Enterprises", "Associates", "Supplies", "Craft", "Mart"]


class ExtractError(ValueError):
    pass


def extract_dir():
    d = Path(getattr(settings, "EXTRACT_DIR", settings.BASE_DIR / "var" / "extracts"))
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---- statistics (aggregates only) -------------------------------------------------------------------------------------


def _hide(n):
    return n if n >= MIN_CELL else f"fewer than {MIN_CELL}"


def statistics_report(scope_path="", concept=None):
    """Aggregate counts for a place and optionally a list type: totals, trust split and a count per direct child place.
    Nothing here names a business."""
    qs = RollupCell.objects.all()
    if concept is not None:
        qs = qs.filter(concept=concept)
    else:
        qs = qs.filter(concept__parent__isnull=True)  # top-level list types only, so nothing is counted twice
    cells = [c for c in qs if scope_path == "" or c.place_path == scope_path]
    total = sum(c.total for c in cells)
    published = sum(c.published for c in cells)
    levels = {}
    for c in cells:
        for k, v in (c.by_level or {}).items():
            levels[k] = levels.get(k, 0) + v
    depth = len(scope_path.split(".")) + 1 if scope_path else 1
    child_rows = {}
    for c in RollupCell.objects.filter(**({"concept": concept} if concept else {"concept__parent__isnull": True})):
        parts = c.place_path.split(".") if c.place_path else []
        if len(parts) != depth:
            continue
        if scope_path and not c.place_path.startswith(scope_path + "."):
            continue
        child_rows[c.place_path] = child_rows.get(c.place_path, 0) + c.published
    return {
        "scope": scope_path or "world",
        "list_type": concept.slug if concept else "all",
        "entries": _hide(total),
        "published": _hide(published),
        "verified_12m": _hide(sum(c.verified_12m for c in cells)),
        "by_level": {k: _hide(v) for k, v in sorted(levels.items())},
        "by_child_place": {k: _hide(v) for k, v in sorted(child_rows.items())},
        "generated_at": clock.now().isoformat(),
        "note": f"Counts below {MIN_CELL} are hidden. No business is named.",
    }


def statistics_csv(report):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["measure", "value"])
    for k in ("scope", "list_type", "entries", "published", "verified_12m"):
        w.writerow([k, report[k]])
    for k, v in report["by_level"].items():
        w.writerow([f"check:{k}", v])
    for k, v in report["by_child_place"].items():
        w.writerow([f"place:{k}", v])
    w.writerow(["note", report["note"]])
    return out.getvalue()


# ---- extracts with trace entries --------------------------------------------------------------------------------------


def extractable(qs):
    """Never exported: people, do-not-share entries, child-facing lists, and anything not published."""
    child = Concept.objects.filter(settings__is_child_facing=True).values_list("pk", flat=True)
    out = []
    for e in qs:
        if e.entity_type == Entry.EntityType.PERSON or "do_not_share" in (e.visibility_flags or []):
            continue
        if e.primary_concept_id in child:
            continue
        out.append(e)
    return out


def trace_count_for(n):
    return min(max(3, math.ceil(n * 0.005)), 25)


def _fake(rng, place_names):
    """A made-up business. The name carries 32 random bits and is never reused by any extract, so a match on the name or
    the website identifies one extract. The address is only there to look real (it has few possible values and is never
    used to identify a leak)."""
    while True:
        name = f"{rng.choice(_ADJ)} {rng.choice(_NOUN)} {secrets.token_hex(4).upper()}"
        if not TraceEntry.objects.filter(name=name).exists():
            break
    slug = name.lower().replace(" ", "-")
    area = rng.choice(place_names) if place_names else "Main Road"
    return name, f"https://www.{slug}.example", f"Plot {rng.randint(2, 98)}, {area}"


def build_extract(actor, scope_path, concept=None, *, order=None, purpose="", buyer_label=""):
    """Write a CSV to the extract directory and return the Extract. Needs a fulfilled extract order or a stated purpose."""
    from accounts.roles import has_cap
    from billing.models import Order

    if not has_cap(actor, "run_extract"):
        raise ExtractError("not allowed")
    if order is not None:
        if order.state != Order.State.FULFILLED or order.product.kind != "extract":
            raise ExtractError("the order is not a paid extract order")
        purpose = purpose or f"order {order.ref}"
    elif not purpose.strip():
        raise ExtractError("state the purpose or give a paid order")
    from places.models import Place

    place = Place.objects.filter(path=scope_path).first()
    if place is None:
        raise ExtractError("unknown place")
    rows_qs = (
        published_entries(place, concept)
        .select_related("place", "primary_concept")
        .prefetch_related("verification_current", "namevariant_set", "place__names")
        .order_by("id")
    )
    entries = extractable(rows_qs)
    if not entries:
        raise ExtractError("nothing to extract for that scope")
    now = clock.now()
    rows = []
    for e in entries:
        alt = e.namevariant_set.all()
        rows.append(
            [
                e.uid,
                e.name,
                alt[0].name if alt else "",
                e.primary_concept.slug,
                e.place.path,
                e.address_text,
                e.website,
                e.status,
                best_level(e, now),
                e.last_verified_at.date().isoformat() if e.last_verified_at else "",
            ]
        )
    import random

    rng = random.Random(secrets.token_bytes(16))
    names = [p.name_for("en") for p in Place.objects.filter(path__startswith=scope_path).prefetch_related("names")[:50]]
    with transaction.atomic():
        ex = Extract.objects.create(
            created_by_id=actor.pk,
            scope_path=scope_path,
            concept=concept,
            order_ref=order.ref if order else "",
            purpose=purpose[:200],
            buyer_label=buyer_label[:120],
            row_count=len(rows),
        )
        base = rows[0]
        traces = []
        for _ in range(trace_count_for(len(rows))):
            n, w, a = _fake(rng, names)
            traces.append(TraceEntry.objects.create(extract=ex, name=n, website=w, address_text=a))
            row = [f"X{secrets.token_hex(4).upper()}", n, "", base[3], base[4], a, w, "open", "ai", base[9]]
            rows.insert(rng.randint(0, len(rows)), row)
        ex.trace_count = len(traces)
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(COLUMNS)
        w.writerows(rows)
        data = out.getvalue()
        ex.sha256 = hashlib.sha256(data.encode()).hexdigest()
        ex.file_name = f"extract-{ex.pk}-{ex.sha256[:8]}.csv"
        (extract_dir() / ex.file_name).write_text(data, encoding="utf-8")
        ex.save()
        audit(
            "extract.create",
            actor=actor,
            object_type="extract",
            object_uid=str(ex.pk),
            payload={"rows": len(entries), "traces": len(traces), "scope": scope_path or "world"},
        )
    return ex


def read_extract(ex, actor):
    """Staff download. Audited every time."""
    from accounts.roles import has_cap

    if not has_cap(actor, "run_extract"):
        raise ExtractError("not allowed")
    audit("extract.download", actor=actor, object_type="extract", object_uid=str(ex.pk))
    return (extract_dir() / ex.file_name).read_bytes()


def identify_leak(text):
    """Which extracts does a pasted sample belong to? Matches a planted name or website, both unique to one extract.
    An address alone never identifies anyone: it has few possible values and two extracts can share one."""
    text_l = text.lower()
    hits = {}
    for t in TraceEntry.objects.select_related("extract"):
        for needle in (t.name, t.website):
            if needle and needle.lower() in text_l:
                hits.setdefault(t.extract_id, set()).add(needle)
    return {k: sorted(v) for k, v in hits.items()}
