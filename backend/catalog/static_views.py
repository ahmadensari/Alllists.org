"""Static pages (plan 8.3.4): about, terms, privacy, plans, sources, how checks work, contributor rules.
They are shared pages like any other: the same bytes for everyone."""

from django.http import Http404

from access.policy import FIELDS
from intake.models import Source

from . import strings
from .views import shell

PAGES = {
    "about": "about",
    "terms": "terms",
    "privacy": "privacy",
    "plans": "plans",
    "sources": "sources",
    "how-checks-work": "how_checks_work",
    "how-lists-are-ordered": "how_ordered",
    "contributors/rules": "contributor_rules",
}

PLAN_ROWS = [  # (field key, label key) in the order shown on the plans page
    ("name", "plan_row_names"),
    ("checks", "plan_row_checks"),
    ("specialities", "plan_row_specialities"),
    ("address", "plan_row_address"),
    ("location", "plan_row_pin"),
    ("website", "plan_row_website"),
    ("social_links", "plan_row_social"),
    ("size", "plan_row_size"),
    ("services", "plan_row_prices"),
    ("certificates", "plan_row_certs"),
    ("enquiry_many", "plan_row_many"),
    ("ads", "plan_row_ads"),
]
WORDS = {
    "full": "plan_full",
    "first3": "plan_first3",
    "area": "plan_area",
    "list": "plan_names",
    "locked": "plan_locked",
    "none": "plan_no",
}


def page(request, key):
    name = PAGES.get(key)
    if name is None:
        raise Http404
    ctx = {
        "title": strings.t(request.lang, f"page_{name}"),
        "robots": "index,follow",
        "canonical": request.build_absolute_uri(request.prefix + "/" + key + "/"),
        "page_key": key,
    }
    stamp = "static"
    if name == "plans":
        ctx["rows"] = [(label, FIELDS[field][0], FIELDS[field][1], FIELDS[field][2]) for field, label in PLAN_ROWS]
        ctx["words"] = WORDS
    if name == "sources":
        sources = list(Source.objects.filter(status="active").exclude(tier="red").order_by("name"))
        ctx["sources"] = [s for s in sources if s.attribution_text or s.licence_text]
        stamp = max([str(s.reviewed_on) for s in sources if s.reviewed_on] or ["0"])
    return shell(request, f"catalog/pages/{name}.html", ctx, stamp)
