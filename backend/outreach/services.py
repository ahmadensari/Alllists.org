"""Relay, opt-in, OTP and suppression (plan 13). Contact values are used here only to deliver and never returned."""

import hashlib
import re
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from core import clock
from core.crypto import encrypt, keyed_hash
from core.models import audit
from entries.models import Contact, Entry

from .models import ClaimOtp, Enquiry, EnquiryRecipient, Optin, OutboxMessage, Suppression

MAX_TEXT = 2000
MAX_ENQUIRIES_PER_DAY = 20
OTP_MINUTES = 15
OTP_MAX_ATTEMPTS = 5
OTP_MAX_PER_HOUR = 3

_PHONE = re.compile(r"(?:\+?\d[\s().\-]*){7,}")
_EMAIL = re.compile(r"[\w.+\-]+\s*(?:@|\(at\)|\[at\])\s*[\w\-]+(?:\s*(?:\.|\(dot\))\s*[\w\-]+)+", re.I)
_URL = re.compile(r"(?:https?://|www\.|\b(?:bit\.ly|t\.me|wa\.me|wa\.link|tinyurl\.com|goo\.gl|linktr\.ee)/)", re.I)
_DIGIT_WORDS = re.compile(
    r"\b(?:zero|one|two|three|four|five|six|seven|eight|nine)"
    r"(?:[\s,-]+(?:zero|one|two|three|four|five|six|seven|eight|nine)){5,}\b",
    re.I,
)


class RelayError(ValueError):
    pass


def contact_leaks(text):
    """Reasons a free-text message could pass contact details around the relay (threat 4). Empty list means clean."""
    found = []
    if _PHONE.search(text):
        found.append("a phone number")
    if _EMAIL.search(text):
        found.append("an email address")
    if _URL.search(text):
        found.append("a link")
    if _DIGIT_WORDS.search(text):
        found.append("a number written in words")
    return found


def normalized_hash(kind, value, country=""):
    from entries.services import normalize_contact

    return keyed_hash(f"{kind}:{normalize_contact(kind, value, country)}")


def is_suppressed(value_hash, channel=""):
    qs = Suppression.objects.filter(value_hash=value_hash)
    return qs.filter(channel="").exists() or (channel and qs.filter(channel=channel).exists())


def suppress(value_hash, channel="", reason="opt_out"):
    Suppression.objects.get_or_create(value_hash=value_hash, channel=channel, defaults={"reason": reason})


def _channel_of(contact):
    return {"email": "email", "whatsapp": "whatsapp"}.get(contact.kind, "sms")


@transaction.atomic
def record_optin(contact, *, method, wording_version, evidence="", topics=()):
    if is_suppressed(contact.value_hash, _channel_of(contact)):
        raise RelayError("this contact is on the do-not-contact list")
    row = Optin.objects.create(
        contact=contact,
        channel=_channel_of(contact),
        method=method,
        topics=list(topics),
        wording_version=wording_version,
        evidence_text=evidence[:200],
    )
    contact.optin_state = "optin"
    contact.save(update_fields=["optin_state"])
    audit(
        "optin.record",
        object_type="contact",
        object_uid=str(contact.pk),
        country_code=contact.country_code,
        payload={"channel": row.channel, "method": method},
    )
    return row


@transaction.atomic
def opt_out(contact, *, reason="opt_out"):
    """One tap: suppression is written first, then the opt-in is withdrawn. Takes effect immediately."""
    suppress(contact.value_hash, "", reason)
    Optin.objects.filter(contact=contact, withdrawn_at__isnull=True).update(withdrawn_at=clock.now())
    contact.optin_state = "withdrawn"
    contact.save(update_fields=["optin_state"])
    audit("optin.withdraw", object_type="contact", object_uid=str(contact.pk), country_code=contact.country_code)


def optout_token(contact):
    """Opaque token for the one-tap opt-out link; derived from the keyed hash so it cannot be guessed."""
    return hashlib.sha256(f"optout:{contact.pk}:{contact.value_hash}".encode()).hexdigest()[:40] + f"-{contact.pk}"


def contact_from_optout_token(token):
    try:
        digest, _, pk = token.rpartition("-")
        contact = Contact.objects.filter(pk=int(pk)).first()
    except ValueError:
        return None
    return contact if contact and optout_token(contact) == token else None


# ---- claim OTP ------------------------------------------------------------------------------------------------------


def _code_hash(entry_id, user_id, code):
    return keyed_hash(f"otp:{entry_id}:{user_id}:{code}")


@transaction.atomic
def send_claim_otp(entry, user, contact):
    """Send a code to a stored contact without revealing it. Returns the channel used."""
    if contact.entry_id != entry.pk:
        raise RelayError("contact does not belong to this entry")
    if is_suppressed(contact.value_hash, _channel_of(contact)):
        raise RelayError("this contact asked not to be contacted")
    recent = ClaimOtp.objects.filter(entry=entry, user=user, expires_at__gt=clock.now() - timedelta(minutes=45))
    if recent.count() >= OTP_MAX_PER_HOUR:
        raise RelayError("too many codes requested; wait and try again")
    code = f"{secrets.randbelow(10**6):06d}"
    ClaimOtp.objects.create(
        entry=entry,
        user=user,
        contact=contact,
        code_hash=_code_hash(entry.pk, user.pk, code),
        expires_at=clock.now() + timedelta(minutes=OTP_MINUTES),
    )
    body = f"Your AllLists code for {entry.name} is {code}. It works for {OTP_MINUTES} minutes."
    if contact.kind == "email":
        send_mail("Your AllLists code", body, None, [contact.value_enc])
    else:
        OutboxMessage.objects.create(channel=_channel_of(contact), kind="otp", contact=contact, body=body)
    audit("claim.otp_sent", actor=user, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return _channel_of(contact)


@transaction.atomic
def verify_claim_otp(entry, user, code):
    """Return the contact the code was sent to, or None. Five wrong tries burn the code."""
    otp = (
        ClaimOtp.objects.select_for_update()
        .filter(entry=entry, user=user, used_at__isnull=True, expires_at__gt=clock.now())
        .order_by("-id")
        .first()
    )
    if otp is None or otp.attempts >= OTP_MAX_ATTEMPTS:
        return None
    otp.attempts += 1
    if secrets.compare_digest(otp.code_hash, _code_hash(entry.pk, user.pk, (code or "").strip())):
        otp.used_at = clock.now()
        otp.save()
        return otp.contact
    otp.save()
    return None


# ---- enquiry relay ----------------------------------------------------------------------------------------------------


@transaction.atomic
def send_enquiry(sender, entries, text, reply_to, *, allow_many=False, scope_path=""):
    """Relay one message to the entries' opted-in contacts. The sender sees counts, never contact data."""
    text = (text or "").strip()
    if not text or len(text) > MAX_TEXT:
        raise RelayError(f"write a message of 1 to {MAX_TEXT} characters")
    leaks = contact_leaks(text)
    if leaks:
        raise RelayError(
            "Remove " + ", ".join(leaks) + " from your message. Replies reach you by email through AllLists."
        )
    if "@" not in (reply_to or ""):
        raise RelayError("a reply email address is needed")
    entries = list(entries)
    if not entries:
        raise RelayError("choose at least one business")
    if len(entries) > 1 and not allow_many:
        raise RelayError("sending to several businesses is for subscribers")
    if len(entries) > 50:
        raise RelayError("at most 50 businesses at a time")
    since = clock.now() - timedelta(days=1)
    if Enquiry.objects.filter(sender=sender, created_at__gte=since).count() >= MAX_ENQUIRIES_PER_DAY:
        raise RelayError("daily limit reached")
    enq = Enquiry.objects.create(
        sender=sender, text=text, reply_to_enc=encrypt(reply_to.strip().lower()), scope_path=scope_path
    )
    counts = {"delivered": 0, "queued": 0, "not_reachable": 0, "suppressed": 0}
    for e in entries:
        if e.publish_state != Entry.PublishState.PUBLISHED or e.status == Entry.Status.PERM_CLOSED:
            state = EnquiryRecipient.State.NOT_REACHABLE
        else:
            state = _deliver(enq, e, reply_to.strip().lower())
        EnquiryRecipient.objects.create(enquiry=enq, entry=e, state=state)
        counts[state] += 1
    audit("enquiry.send", actor=sender, object_type="enquiry", object_uid=str(enq.pk), payload=counts)
    return enq, counts


def _deliver(enq, entry, reply_to):
    contacts = [c for c in entry.contact_set.filter(optin_state="optin")]
    if any(is_suppressed(c.value_hash) for c in contacts):
        return EnquiryRecipient.State.SUPPRESSED
    for c in contacts:
        if c.kind == "email":
            body = (
                f"{enq.text}\n\n--\nSent through AllLists. Reply to this email to answer.\n"
                f"Stop these messages: {settings.SITE_URL}/optout/{optout_token(c)}/\n"
            )
            send_mail(f"Enquiry for {entry.name} via AllLists", body, None, [c.value_enc])
            return EnquiryRecipient.State.DELIVERED
    for c in contacts:
        OutboxMessage.objects.create(
            channel=_channel_of(c),
            kind="enquiry",
            contact=c,
            body=f"{enq.text}\nReply to: {reply_to}\nStop: {settings.SITE_URL}/optout/{optout_token(c)}/",
        )
        return EnquiryRecipient.State.QUEUED
    return EnquiryRecipient.State.NOT_REACHABLE
