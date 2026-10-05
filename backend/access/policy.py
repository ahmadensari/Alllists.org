"""One table decides what each viewer may see (plan 9.1, appendix C.4, rule R03). Views and fragments call `visible()`
and nothing else decides visibility. Contacts are absent on purpose: they are never shown (rule R02)."""

from dataclasses import dataclass
from typing import Optional

# value meanings: "full" shown in full; "area" place name only; "names" names only; "first3" first three items;
# "list" names of items without detail; "locked" present but locked (one panel names it); "none" not shown
FREE_OWN, FREE_WIDER, SUBSCRIBER = 0, 1, 2

FIELDS = {
    "name": ("full", "full", "full"),
    "name_variants": ("full", "full", "full"),
    "entity_type": ("full", "none", "full"),
    "category": ("full", "full", "full"),
    "area": ("full", "full", "full"),
    "specialities": ("first3", "none", "full"),
    "checks": ("full", "full", "full"),
    "status": ("full", "full", "full"),
    "company_tag": ("full", "full", "full"),
    "free_details": ("full", "none", "full"),  # hours, languages, year established, business type, OEM
    "address": ("area", "none", "full"),
    "location": ("area", "none", "full"),
    "website": ("locked", "none", "full"),
    "social_links": ("locked", "none", "full"),
    "size": ("locked", "none", "full"),
    "markets": ("locked", "none", "full"),
    "min_order": ("locked", "none", "full"),
    "services": ("list", "none", "full"),  # names free, prices with dates for subscribers
    "products": ("locked", "none", "full"),
    "certificates": ("list", "none", "full"),  # names free, details for subscribers
    "company_sections": ("full", "none", "full"),
    "enquiry_one": ("full", "full", "full"),  # entry pages are not scope-limited; only list rows are
    "enquiry_many": ("none", "none", "full"),
    "ads": ("full", "full", "none"),
}


@dataclass(frozen=True)
class Viewer:
    subscriber: bool = False
    own_path: Optional[str] = None  # the viewer's own place subtree (chosen place, else edge guess)


def scope_of(viewer, place_path):
    """ "own" when the list's place is inside the viewer's own place subtree, else "wider" (rule R04).
    Unknown own place counts as wider, the safe side."""
    own = viewer.own_path
    if own is None:
        return "wider"
    if place_path == own or place_path.startswith(own + "."):
        return "own"
    return "wider"


def visible(field, viewer, place_path):
    """Return the visibility value for a field. Unknown fields are not shown."""
    row = FIELDS.get(field)
    if row is None:
        return "none"
    if viewer.subscriber:
        return row[SUBSCRIBER]
    return row[FREE_OWN] if scope_of(viewer, place_path) == "own" else row[FREE_WIDER]


def list_mode(viewer, place_path):
    """How a list page's rows render for this viewer: "full" (subscriber), "free" (own place) or "names" (wider)."""
    if viewer.subscriber:
        return "full"
    return "free" if scope_of(viewer, place_path) == "own" else "names"
