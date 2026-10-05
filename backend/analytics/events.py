from access.quotas import subject_for

from .models import Event

NAMES = {
    "list_view",
    "entry_view",
    "place_view",
    "search",
    "search_zero_result",
    "share_click",
    "enquiry_sent",
    "claim_started",
    "claim_completed",
    "optin_recorded",
    "report_submitted",
    "removal_requested",
    "subscribe_click",
    "subscription_started",
    "quota_hit",
    "contributor_signup",
    "entry_added",
    "task_completed",
    "verification_recorded",
    "ref_visit",
}


def emit(name, request=None, **props):
    """Record an event. Unknown names are refused so the catalogue in the plan stays the single list."""
    if name not in NAMES:
        raise ValueError(f"unknown event {name!r}")
    subject = subject_for(request)[0] if request is not None else ""
    return Event.objects.create(name=name, subject_hash=subject, props=props)
