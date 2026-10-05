"""Campaign service (plan 13.2, phase P4): opt-in only, approved templates, verified suppliers, per-country switch,
caps, quiet hours, delivery tracking, auto-pause and a cost-per-reply report. Contacts are used to send and never returned.
"""

import hmac
import json
import re
from datetime import timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import transaction
from django.db.models import Count, Q

from core import clock
from core.models import CountrySwitch, audit
from entries.models import Entry

from . import services as relay
from .models import Campaign, DeliveryEvent, Message, Optin, SupplierVerification

VAR_NAMES = ("company", "category", "note")
MAX_VAR = 200


class CampaignError(ValueError):
    pass


def render_template(template, variables):
    """Fill the approved template. Variables are limited to named ones, length-capped and scanned for contact details."""
    out = template.body
    for name in VAR_NAMES:
        value = (variables.get(name) or "").strip()
        if len(value) > MAX_VAR:
            raise CampaignError(f"{name} is too long")
        leaks = relay.contact_leaks(value)
        if leaks:
            raise CampaignError(f"remove {', '.join(leaks)} from {name}")
        out = out.replace("{" + name + "}", value)
    if re.search(r"\{\w+\}", out):
        raise CampaignError("the template needs a value for every placeholder")
    return out


def supplier_verified(user):
    sv = SupplierVerification.objects.filter(user=user).first()
    return bool(sv and sv.state == "verified")


@transaction.atomic
def request_supplier_verification(user, company):
    sv, _ = SupplierVerification.objects.get_or_create(user=user, defaults={"company": company[:120]})
    return sv


@transaction.atomic
def decide_supplier(sv, *, actor, approve, note=""):
    sv.state, sv.decided_by_id, sv.decided_at, sv.note = (
        ("verified" if approve else "rejected"),
        actor.pk,
        clock.now(),
        note[:200],
    )
    sv.save()
    audit("supplier.decide", actor=actor, object_type="user", object_uid=str(sv.user_id), payload={"approved": approve})
    return sv


def country_ready(country_code, channel):
    sw = CountrySwitch.for_country(country_code)
    return sw.outreach_on and channel in (sw.outreach_channels or [])


def local_hour(country_code, now):
    tz = settings.OUTREACH_TZ.get(country_code.upper())
    return now.astimezone(ZoneInfo(tz)).hour if tz else now.hour


def in_quiet_hours(country_code, now):
    start, end = settings.OUTREACH_QUIET_WINDOW.get(country_code.upper(), settings.OUTREACH_DEFAULT_WINDOW)
    return not (start <= local_hour(country_code, now) < end)


def recipients(scope_path, concept, channel):
    """[(entry, contact)] with a live opt-in for the channel, not suppressed. Caps are applied at send time."""
    from analytics.rollups import descendant_concept_ids

    kinds = {"email": ["email"], "whatsapp": ["whatsapp", "mobile"], "sms": ["phone", "mobile"]}[channel]
    ids = descendant_concept_ids(concept.pk)
    qs = Entry.objects.filter(
        publish_state="published", deleted_at__isnull=True, merged_into__isnull=True, primary_concept_id__in=ids
    ).filter(Q(place_path=scope_path) | Q(place_path__startswith=scope_path + ".") if scope_path else Q())
    out = []
    for e in qs:
        for c in e.contact_set.filter(kind__in=kinds, optin_state="optin"):
            if (
                not relay.is_suppressed(c.value_hash, channel)
                and Optin.objects.filter(contact=c, withdrawn_at__isnull=True).exists()
            ):
                out.append((e, c))
                break
    return out


def estimate_cost(channel, n):
    return settings.OUTREACH_PRICE_MINOR[channel] * n


@transaction.atomic
def create_campaign(buyer, *, scope_path, concept, template, channel, variables, budget_minor):
    if settings.OUTREACH_SHARE_PERCENT is None:
        raise CampaignError("the contributor share for outreach is not set yet, so paid outreach cannot start")
    if not supplier_verified(buyer):
        raise CampaignError("your company must be verified before you can send campaigns")
    country = scope_path.split(".")[0].upper() if scope_path else ""
    if not country_ready(country, channel):
        raise CampaignError("outreach is not open for this country and channel")
    if template.provider_state != "approved" or template.channel != channel:
        raise CampaignError("choose an approved template for this channel")
    render_template(template, variables)
    n = len(recipients(scope_path, concept, channel))
    if n == 0:
        raise CampaignError("nobody in this list has opted in to this channel yet")
    if budget_minor < estimate_cost(channel, n):
        raise CampaignError(f"the budget does not cover {n} messages")
    c = Campaign.objects.create(
        buyer=buyer,
        scope_path=scope_path,
        concept=concept,
        template=template,
        variables=variables,
        channel=channel,
        country_code=country,
        budget_minor=budget_minor,
        status=Campaign.Status.PENDING,
    )
    audit(
        "campaign.create",
        actor=buyer,
        object_type="campaign",
        object_uid=str(c.pk),
        country_code=country,
        payload={"n": n},
    )
    return c


@transaction.atomic
def approve_campaign(campaign, *, actor):
    if campaign.status != Campaign.Status.PENDING:
        raise CampaignError("only pending campaigns can be approved")
    campaign.status, campaign.approved_by_id = Campaign.Status.APPROVED, actor.pk
    campaign.save(update_fields=["status", "approved_by_id"])
    audit("campaign.approve", actor=actor, object_type="campaign", object_uid=str(campaign.pk))
    return campaign


def _sent_this_week(contact, now):
    return Message.objects.filter(contact=contact, ts__gte=now - timedelta(days=7)).exclude(state="failed").count()


def _sent_today(buyer, now):
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return Message.objects.filter(campaign__buyer=buyer, ts__gte=start).exclude(state="failed").count()


@transaction.atomic
def send_batch(campaign, provider, *, now=None, limit=200):
    """Send what the rules allow right now and return counts. Anything held back stays for the next run."""
    now = now or clock.now()
    if campaign.status not in (Campaign.Status.APPROVED, Campaign.Status.SENDING):
        raise CampaignError("campaign is not approved")
    if not campaign.funded:
        raise CampaignError("campaign is not funded")
    if not country_ready(campaign.country_code, campaign.channel):
        return _pause(campaign, "country switch is off")
    counts = {"sent": 0, "held_quiet": 0, "held_cap": 0, "skipped": 0}
    if in_quiet_hours(campaign.country_code, now):
        counts["held_quiet"] = len(recipients(campaign.scope_path, campaign.concept, campaign.channel))
        return counts
    body = render_template(campaign.template, campaign.variables)
    unit = settings.OUTREACH_PRICE_MINOR[campaign.channel]
    done = set(campaign.messages.values_list("contact_id", flat=True))
    campaign.status = Campaign.Status.SENDING
    for entry, contact in recipients(campaign.scope_path, campaign.concept, campaign.channel):
        if counts["sent"] >= limit:
            break
        if contact.pk in done:
            counts["skipped"] += 1
            continue
        if campaign.spent_minor + unit > campaign.budget_minor:
            break
        if (
            _sent_this_week(contact, now) >= settings.OUTREACH_WEEKLY_CAP_PER_SHOP
            or _sent_today(campaign.buyer, now) >= settings.OUTREACH_DAILY_CAP_PER_SENDER
        ):
            counts["held_cap"] += 1
            continue
        footer = f"\nStop messages: {settings.SITE_URL}/optout/{relay.optout_token(contact)}/"
        pid = provider.send(
            channel=campaign.channel, to=contact.value_enc, body=body + footer, template_key=campaign.template.key
        )
        Message.objects.create(
            campaign=campaign,
            entry=entry,
            contact=contact,
            channel=campaign.channel,
            state="sent",
            provider_id=pid,
            cost_minor=unit,
            ts=now,
        )
        campaign.spent_minor += unit
        counts["sent"] += 1
    campaign.save()
    check_health(campaign)
    return counts


def _pause(campaign, reason):
    campaign.status, campaign.pause_reason = Campaign.Status.PAUSED, reason[:120]
    campaign.save(update_fields=["status", "pause_reason"])
    audit("campaign.pause", object_type="campaign", object_uid=str(campaign.pk), payload={"reason": reason})
    return {"paused": reason}


def check_health(campaign):
    """Pause the campaign and its sender when opt-outs exceed 2 percent or failures exceed 10 percent (rule R29)."""
    total = campaign.messages.exclude(state="queued").count()
    if total < settings.OUTREACH_PAUSE_MIN_SAMPLE:
        return False
    optout = campaign.messages.filter(state="opted_out").count() / total
    failed = campaign.messages.filter(state="failed").count() / total
    if optout > settings.OUTREACH_PAUSE_OPTOUT or failed > settings.OUTREACH_PAUSE_FAILURE:
        _pause(campaign, f"opt-out {optout:.1%} or failure {failed:.1%} over the limit")
        SupplierVerification.objects.filter(user=campaign.buyer, state="verified").update(state="paused")
        return True
    return False


# ---- provider callbacks ----------------------------------------------------------------------------------------------------


def sign(secret, body):
    import hashlib

    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


@transaction.atomic
def handle_callback(provider, body, signature):
    """Delivery, read, reply, failure and stop events from a provider. Signed, idempotent per (message, event, ts)."""
    secret = settings.MESSAGING_WEBHOOK_SECRETS.get(provider)
    if not secret:
        return 404, "unknown provider"
    if not signature or not hmac.compare_digest(sign(secret, body), signature):
        return 401, "bad signature"
    try:
        data = json.loads(body)
        msg = Message.objects.select_for_update().get(provider_id=data["message_id"])
        event = data["event"]
    except (ValueError, KeyError, Message.DoesNotExist):
        return 400, "bad payload"
    if event not in ("delivered", "read", "replied", "failed", "opted_out"):
        return 400, "unknown event"
    if DeliveryEvent.objects.filter(message=msg, event=event).exists():
        return 200, "duplicate"
    DeliveryEvent.objects.create(message=msg, event=event, payload={k: v for k, v in data.items() if k != "reply"})
    order = ["queued", "sent", "delivered", "read", "replied"]
    if event in order and order.index(event) > order.index(msg.state if msg.state in order else "queued"):
        msg.state = event
    if event == "replied":
        msg.reply_text = (data.get("reply") or "")[:2000]
    if event == "failed":
        msg.state = "failed"
    if event == "opted_out":
        msg.state = "opted_out"
        relay.opt_out(msg.contact, reason="campaign_stop")
    msg.save()
    check_health(msg.campaign)
    return 200, "recorded"


# ---- report ----------------------------------------


def report(campaign):
    c = campaign.messages.aggregate(
        total=Count("id"),
        delivered=Count("id", filter=Q(state__in=["delivered", "read", "replied"])),
        replied=Count("id", filter=Q(state="replied")),
        failed=Count("id", filter=Q(state="failed")),
        opted_out=Count("id", filter=Q(state="opted_out")),
    )
    c["spent_minor"] = campaign.spent_minor
    c["cost_per_reply_minor"] = (campaign.spent_minor / c["replied"]) if c["replied"] else None
    c["reply_rate"] = (c["replied"] / c["total"]) if c["total"] else None
    return c
