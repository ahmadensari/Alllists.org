"""Data-subject rights (plan P3.14): the consent register, subject access, and an account holder's own data.

Subject access is run by staff for a requester who proves they hold the contact value; we never show the stored value,
only that we hold something of that kind, and nothing is returned to an unverified visitor."""

import json

from django.db import transaction

from core import clock
from core.models import audit
from entries import services as es
from entries.models import Contact, Entry
from outreach.models import Enquiry, EnquiryRecipient, Optin, Suppression
from outreach.services import normalized_hash, opt_out

from .models import Report, Takedown


def _mask(kind, value_hash):
    return f"{kind} on file (reference {value_hash[:6]})"


def subject_access_report(kind, value, country=""):
    """Everything we hold that is linked to one contact value, as a dict. Raises nothing; empty means nothing found."""
    h = normalized_hash(kind, value, country)
    contacts = list(Contact.objects.filter(value_hash=h).select_related("entry"))
    out = {
        "generated_at": clock.now().isoformat(),
        "contact_reference": h[:6],
        "on_do_not_contact_list": Suppression.objects.filter(value_hash=h).exists(),
        "entries": [],
    }
    for c in contacts:
        e = c.entry
        out["entries"].append(
            {
                "code": e.uid,
                "name": e.name,
                "place": e.place_path,
                "list_type": e.primary_concept.slug,
                "publish_state": e.publish_state,
                "status": e.status,
                "created_via": e.created_via,
                "source": e.source.name if e.source_id else "",
                "contact": _mask(c.kind, c.value_hash),
                "opt_in": [
                    {
                        "channel": o.channel,
                        "method": o.method,
                        "wording": o.wording_version,
                        "at": o.created_at.isoformat(),
                        "withdrawn": o.withdrawn_at.isoformat() if o.withdrawn_at else None,
                    }
                    for o in Optin.objects.filter(contact=c)
                ],
                "consent": [
                    {"status": r.status, "method": r.method, "wording": r.wording_version, "at": r.at.isoformat()}
                    for r in e.consents.all()
                ],
                "checks": [
                    {
                        "level": v.level,
                        "state": v.state,
                        "field_group": v.field_group,
                        "expires": v.expires_at.isoformat() if v.expires_at else None,
                    }
                    for v in e.verification_current.all()
                ],
                "enquiries_relayed": EnquiryRecipient.objects.filter(entry=e).count(),
                "reports_about_it": Report.objects.filter(entry=e).count(),
            }
        )
    audit("subject_access.run", object_type="contact", object_uid=h[:12], payload={"entries": len(out["entries"])})
    return out


def subject_access_json(report):
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)


@transaction.atomic
def withdraw_consent(entry, *, actor, method="staff"):
    """A person withdraws consent: it is recorded, the entry leaves public view, its contacts go on the suppression list
    and no re-import can bring it back."""
    es.record_consent(entry, status="withdrawn", method=method, wording_version="withdraw-v1", actor=actor)
    for c in entry.contact_set.all():
        opt_out(c, reason="consent_withdrawn")
    entry.publish_state = Entry.PublishState.SUPPRESSED
    entry.save(update_fields=["publish_state"])
    audit("consent.withdraw", actor=actor, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return entry


def consent_register():
    """Latest consent record per entry that has one, newest first (for the staff register)."""
    from entries.models import ConsentRecord

    latest = {}
    for r in ConsentRecord.objects.select_related("entry").order_by("id"):
        latest[r.entry_id] = r
    return sorted(latest.values(), key=lambda r: r.at, reverse=True)


def account_data(user):
    """An account holder's own data as a dict (portability). Contact values of other people are never included."""
    from billing.models import Order
    from volunteers.models import ContributorProfile, Reward

    prof = getattr(user, "profile", None)
    contributor = ContributorProfile.objects.filter(user=user).first()
    return {
        "generated_at": clock.now().isoformat(),
        "account": {
            "username": user.username,
            "email": user.email,
            "joined": user.date_joined.isoformat(),
            "display_name": getattr(prof, "display_name", ""),
            "language": getattr(prof, "lang", ""),
        },
        "contributor": (
            {"level": contributor.level, "points": contributor.points, "ref_code": contributor.ref_code}
            if contributor
            else None
        ),
        "rewards": [
            {"kind": r.kind, "detail": r.detail, "at": r.granted_at.isoformat()}
            for r in Reward.objects.filter(user=user)
        ],
        "entries_added": [
            {"code": e.uid, "name": e.name, "place": e.place_path, "state": e.publish_state}
            for e in Entry.objects.filter(created_by=user)
        ],
        "enquiries": [
            {"at": q.created_at.isoformat(), "text": q.text, "businesses": q.recipients.count()}
            for q in Enquiry.objects.filter(sender=user)
        ],
        "orders": [
            {
                "ref": o.ref,
                "product": o.product.name,
                "amount_minor": o.amount_minor,
                "currency": o.currency,
                "state": o.state,
            }
            for o in Order.objects.filter(buyer=user).select_related("product")
        ],
        "subscriptions": [
            {
                "plan": s.plan.key,
                "scope": s.scope_path,
                "from": s.period_start.isoformat(),
                "to": s.period_end.isoformat(),
            }
            for s in user.subscriptions.select_related("plan")
        ],
    }


def open_takedowns():
    return Takedown.objects.filter(state="open")
