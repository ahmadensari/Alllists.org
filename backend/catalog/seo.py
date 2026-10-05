"""Search-engine rules in code (plan 8.6, rule R23)."""

import json
from urllib.parse import urlencode

from django.conf import settings

from core.models import CountrySwitch
from entries.models import Entry

from . import strings

FILTER_PARAMS = ("area", "sort", "q", "page", "view")


def canonical_path(path):
    return path


def indexable_list(place, concept, cell, params):
    """A list page is indexable only with enough verified entries, an allowing country switch, and no filter or sort."""
    if any(params.get(p) for p in FILTER_PARAMS):
        return False
    threshold = getattr(getattr(concept, "settings", None), "index_threshold", settings.INDEX_THRESHOLD)
    verified = cell["by_level"].get("surveyor", 0) + cell["by_level"].get("owner", 0)
    country = place.country_code
    if not country or not CountrySwitch.for_country(country).indexing_on:
        return False
    return verified >= threshold


def indexable_entry(entry, level):
    """Entry pages index only when verified by a person and rich enough (plan decision Q-T3 default)."""
    if entry.publish_state != Entry.PublishState.PUBLISHED or level not in ("surveyor", "owner"):
        return False
    if "noindex" in (entry.visibility_flags or []) or entry.entity_type == Entry.EntityType.PERSON:
        return False
    if not CountrySwitch.for_country(entry.country_code).indexing_on:
        return False
    rich = entry.service_set.exists() or entry.identifier_set.exists() or entry.hours_set.exists()
    return bool(rich)


def robots_meta(indexable):
    return "index,follow" if indexable else "noindex,follow"


def alternates(request, path):
    base = request.build_absolute_uri("/").rstrip("/")
    return [("en", base + path), ("ur", base + "/ur" + path), ("x-default", base + path)]


def query_string(params, **changes):
    merged = {k: v for k, v in params.items() if v}
    merged.update({k: v for k, v in changes.items()})
    merged = {k: v for k, v in merged.items() if v not in (None, "", 0)}
    return ("?" + urlencode(sorted(merged.items()))) if merged else ""


def jsonld(data):
    # "</" is escaped so the block can never end the script element
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def list_jsonld(lang, title, url, rows):
    return jsonld(
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": title,
            "url": url,
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": r["name"]} for i, r in enumerate(rows)
            ],
        }
    )


def entry_jsonld(entry, place, url):
    return jsonld(
        {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": entry.name,
            "url": url,
            "address": {
                "@type": "PostalAddress",
                "addressLocality": place.name_for("en"),
                "addressCountry": entry.country_code,
            },
        }
    )


def title(lang, key, **kw):
    return strings.t(lang, key, **kw)
