"""Paste and CSV import (plan 7.2): parse, map columns, normalise, create drafts, check for duplicates.
Imported entries are drafts and earn nothing until verified (rules R08, R09)."""

import csv
import io

from django.db import transaction
from django.utils import timezone

from core.models import audit
from core.textfold import fold
from entries import services as es

from . import dedupe
from .gate import assert_allowed
from .models import DedupeCandidate, ImportBatch, ImportRow

# Header words in English, Urdu and Roman Urdu. Compared after folding.
ALIASES = {
    "name": [
        "name",
        "business name",
        "company",
        "company name",
        "firm",
        "shop",
        "title",
        "naam",
        "نام",
        "کمپنی",
        "دکان",
        "فرم",
    ],
    "phone": [
        "phone",
        "mobile",
        "tel",
        "telephone",
        "contact",
        "contact no",
        "number",
        "cell",
        "whatsapp",
        "raabta",
        "فون",
        "موبائل",
        "نمبر",
        "رابطہ",
    ],
    "email": ["email", "e-mail", "mail", "ای میل"],
    "address": ["address", "location", "road", "street", "pata", "پتہ", "علاقہ", "سڑک"],
    "website": ["website", "web", "url", "site", "ویب سائٹ"],
    "specialities": ["products", "speciality", "specialities", "services", "items", "make", "پروڈکٹ", "مصنوعات"],
}
_FOLDED = {field: {fold(a) for a in words} for field, words in ALIASES.items()}


class ImportError_(ValueError):
    pass


def parse_table(text):
    """Pasted text or CSV to (headers, rows as dicts). Tab, comma, semicolon and pipe are detected."""
    text = text.strip("﻿\n\r ")
    if not text:
        raise ImportError_("nothing to import")
    sample = text[:2000]
    delim = max(["\t", ",", ";", "|"], key=sample.count)
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    rows = [r for r in reader if any(c.strip() for c in r)]
    headers, body = [h.strip() for h in rows[0]], rows[1:]
    return headers, [{headers[i]: (r[i].strip() if i < len(r) else "") for i in range(len(headers))} for r in body]


def guess_mapping(headers):
    mapping = {}
    for h in headers:
        for field, names in _FOLDED.items():
            if fold(h) in names and field not in mapping.values():
                mapping[h] = field
                break
    return mapping


def normalise_row(raw, mapping, country_code):
    out = {"name": "", "phones": [], "emails": [], "address": "", "website": "", "specialities": []}
    for header, value in raw.items():
        field = mapping.get(header)
        value = (value or "").strip()
        if not field or not value:
            continue
        if field == "name":
            out["name"] = " ".join(value.split())
        elif field == "phone":
            for part in value.replace("/", ",").replace(";", ",").split(","):
                n = es.normalize_contact("phone", part, country_code)
                if len(n.lstrip("+")) >= 7:
                    out["phones"].append(n)
        elif field == "email":
            out["emails"].append(es.normalize_contact("email", value))
        elif field == "address":
            out["address"] = value
        elif field == "website":
            out["website"] = value if value.startswith("http") else "https://" + value
        elif field == "specialities":
            out["specialities"] = [s.strip() for s in value.replace(";", ",").split(",") if s.strip()]
    return out


@transaction.atomic
def run_import(batch, actor=None, addons=None):
    """Create draft entries for every usable row. Returns the batch counts."""
    if not batch.declared_rights:
        raise ImportError_("the contributor must declare the right to share this list")
    assert_allowed(batch.source, "import")
    headers, rows = parse_table(batch.raw_text)
    batch.mapping = batch.mapping or guess_mapping(headers)
    if "name" not in batch.mapping.values():
        batch.status = ImportBatch.Status.FAILED
        batch.counts = {"error": "no name column found"}
        batch.save()
        raise ImportError_("could not find a name column; set the mapping")
    country = batch.place.country_code
    counts = {"rows": len(rows), "drafted": 0, "duplicate": 0, "possible_duplicate": 0, "error": 0}
    for line_no, raw in enumerate(rows, start=2):
        row = ImportRow.objects.create(batch=batch, line_no=line_no, raw=raw)
        norm = normalise_row(raw, batch.mapping, country)
        row.normalised = norm
        if not norm["name"]:
            row.status, row.message = ImportRow.Status.ERROR, "no name"
            counts["error"] += 1
            row.save()
            continue
        contacts = [("phone", p) for p in dict.fromkeys(norm["phones"])] + [("email", e) for e in norm["emails"]]
        extra = {"addons": addons} if addons else {}
        entry = es.create_entry(
            name=norm["name"],
            place=batch.place,
            primary_concept=batch.concept,
            created_by=batch.uploader,
            created_via="import",
            source=batch.source,
            address_text=norm["address"],
            website=norm["website"],
            contacts=contacts,
            **extra,
        )
        row.entry = entry
        found = dedupe.scan_entry(entry)
        if found and found[0][1] >= dedupe.AUTO_MERGE:
            other, s, _ = found[0]
            es.merge_entries(other, entry, actor=actor, score=s)
            row.entry, row.status, row.message = other, ImportRow.Status.DUPLICATE, f"merged into {other.uid}"
            counts["duplicate"] += 1
        else:
            row.status = ImportRow.Status.DRAFTED
            if found:
                for other, s, f in found:
                    a, b = sorted([entry, other], key=lambda e: e.pk)
                    DedupeCandidate.objects.get_or_create(a_entry=a, b_entry=b, defaults=dict(score=s, features=f))
                row.message = "possible duplicate, queued for review"
                counts["possible_duplicate"] += 1
            counts["drafted"] += 1
        row.save()
    batch.status, batch.counts, batch.finished_at = ImportBatch.Status.DONE, counts, timezone.now()
    batch.save()
    audit(
        "import.run",
        actor=actor,
        object_type="import_batch",
        object_uid=str(batch.pk),
        country_code=country,
        payload=counts,
    )
    return counts
