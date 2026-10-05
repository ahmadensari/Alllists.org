"""Entry service layer: creation, edits with change log, verification state machine, publish rules, claims, consent.

Rules enforced here: R07 (independence, expiry), R08 (draft hidden, publish bar), R09 (credit eligibility),
R18/R19 (person and child-facing gates), R21 (source gate), R02 (contacts encrypted, hashed)."""

import re
from datetime import timedelta

from django.conf import settings
from django.db import transaction

from core import clock
from core.crypto import keyed_hash
from core.models import ChangeLog, CountrySwitch, audit
from core.textfold import fold
from intake.gate import SourceBlocked, assert_allowed
from taxonomy.models import ListTypeSettings
from taxonomy.services import validate_addons

from .models import (
    Claim,
    ConsentRecord,
    Contact,
    CreditEvent,
    Entry,
    NameVariant,
    VerificationCurrent,
    VerificationEvent,
)

LEVEL_ORDER = ["surveyor", "owner", "ai"]
EDITABLE = {
    "name",
    "description",
    "address",
    "address_text",
    "website",
    "size_band",
    "year_established",
    "languages",
    "price_band",
    "payment_methods",
    "addons",
    "status",
    "status_date",
    "lat",
    "lon",
    "precision_class",
    "coord_source",
    "coord_date",
    "service_area",
    "entity_type",
    "place",
}


class EntryError(ValueError):
    pass


class GuardError(EntryError):
    """A verification rule (independence, claim, evidence) was not met."""


def normalize_contact(kind, value, country_code=""):
    value = (value or "").strip()
    if kind == "email":
        return value.lower()
    digits = re.sub(r"[^\d+]", "", value)
    if digits.startswith("00"):
        digits = "+" + digits[2:]
    if not digits.startswith("+") and country_code == "PK" and digits.startswith("0"):
        digits = "+92" + digits[1:]
    return digits


@transaction.atomic
def create_entry(
    *,
    name,
    place,
    primary_concept,
    created_by=None,
    created_via=Entry.CreatedVia.CONTRIBUTOR,
    source=None,
    contacts=(),
    name_variants=(),
    **fields,
):
    if created_via in (Entry.CreatedVia.IMPORT, Entry.CreatedVia.AGENT, Entry.CreatedVia.REGISTER):
        assert_allowed(source, "import" if created_via != Entry.CreatedVia.AGENT else "agent_fetch")
    from outreach.services import is_suppressed, normalized_hash  # late import: outreach depends on entries

    for kind, value in contacts:
        if is_suppressed(normalized_hash(kind, value, place.country_code)):
            raise EntryError("this contact asked to be removed and cannot be added again")
    addons = fields.get("addons") or {}
    if primary_concept.template_id:
        problems = validate_addons(primary_concept.template, addons)
        if problems:
            raise EntryError(f"invalid add-on values: {problems}")
        fields["addon_template_version"] = primary_concept.template.version
    elif addons:
        raise EntryError("this list type has no add-on template")
    country = place.country_code or "ZZ"
    entry = Entry.objects.create(
        name=name,
        name_fold=fold(name),
        place=place,
        place_path=place.path,
        country_code=country,
        primary_concept=primary_concept,
        entity_type=fields.pop("entity_type", primary_concept.entity_type_default),
        created_by=created_by,
        created_via=created_via,
        source=source,
        **fields,
    )
    for text, lang, kind in name_variants:
        NameVariant.objects.create(
            entry=entry, country_code=country, text=text, language=lang, kind=kind, text_fold=fold(text)
        )
    for kind, value in contacts:
        add_contact(entry, kind, value)
    ChangeLog.objects.create(
        entry_id=entry.pk,
        country_code=country,
        field_key="created",
        new={"name": name},
        actor_id=getattr(created_by, "pk", None),
        source_id=getattr(source, "pk", None),
    )
    if created_by is not None:
        CreditEvent.objects.create(
            entry=entry, user=created_by, kind="added", eligible=False, ineligible_reason="unverified"
        )
    audit(
        "entry.create",
        actor=created_by,
        object_type="entry",
        object_uid=entry.uid,
        country_code=country,
        payload={"via": created_via},
    )
    return entry


def add_contact(entry, kind, value):
    norm = normalize_contact(kind, value, entry.country_code)
    return Contact.objects.create(
        entry=entry, country_code=entry.country_code, kind=kind, value_enc=norm, value_hash=keyed_hash(f"{kind}:{norm}")
    )


@transaction.atomic
def update_entry(entry, *, actor=None, **changes):
    bad = set(changes) - EDITABLE
    if bad:
        raise EntryError(f"fields not editable here: {sorted(bad)}")
    for key, new in changes.items():
        old = getattr(entry, key)
        if old == new:
            continue
        if key == "place":
            entry.place_path = new.path
            old, new_log = old.uid, new.uid
        else:
            new_log = new
        setattr(entry, key, new)
        if key == "name":
            entry.name_fold = fold(new)
        ChangeLog.objects.create(
            entry_id=entry.pk,
            country_code=entry.country_code,
            field_key=key,
            old=_jsonable(old),
            new=_jsonable(new_log),
            actor_id=getattr(actor, "pk", None),
        )
    entry.save()
    audit(
        "entry.update",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"fields": sorted(changes)},
    )
    return entry


def _jsonable(v):
    return v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v)


# ---- verification -------------------------------------------------------------------------------------------


def current_level(entry, now=None):
    """Best unexpired check level, or "none". Levels are independent chips; this is the best one for list order."""
    now = now or clock.now()
    levels = {v.level for v in VerificationCurrent.objects.filter(entry=entry, state="verified", expires_at__gt=now)}
    for lv in LEVEL_ORDER:
        if lv in levels:
            return lv
    return "none"


def current_levels(entry, now=None):
    now = now or clock.now()
    return {v.level for v in VerificationCurrent.objects.filter(entry=entry, state="verified", expires_at__gt=now)}


@transaction.atomic
def record_verification(entry, *, field_group, level, actor=None, method="", evidence="", source=None, now=None):
    now = now or clock.now()
    if level not in LEVEL_ORDER:
        raise GuardError(f"unknown level {level!r}")
    if level in ("surveyor", "owner"):
        if actor is None:
            raise GuardError("a person must record a surveyor or owner check")
        if not method or not evidence.strip():
            raise GuardError("method and evidence text are required")
    if level == "surveyor" and entry.created_by_id and actor.pk == entry.created_by_id:
        raise GuardError("a surveyor never verifies an entry they added (rule R07)")
    if level == "owner":
        if entry.claim_state != Entry.ClaimState.CLAIMED:
            raise GuardError("owner check needs a successful claim")
        if not Claim.objects.filter(entry=entry, user=actor, state=Claim.State.APPROVED).exists():
            raise GuardError("actor is not the approved claimant")
    if level == "ai":
        if source is None:
            raise GuardError("an AI check must name its source")
        if entry.source_id is not None and source.pk == entry.source_id:
            raise GuardError("an AI check must use a different source from the draft (rule R07)")
        assert_allowed(source, "agent_fetch")
        if not evidence.strip():
            raise GuardError("an AI check must store its evidence")
    days = settings.CHECK_VALIDITY_DAYS[level]
    previous = (
        VerificationEvent.objects.filter(entry=entry, field_group=field_group, level=level).order_by("-id").first()
    )
    event = VerificationEvent.objects.create(
        entry=entry,
        country_code=entry.country_code,
        field_group=field_group,
        level=level,
        state="verified",
        actor_id=getattr(actor, "pk", None),
        method=method,
        evidence_text=evidence,
        source=source,
        ts=now,
        expires_at=now + timedelta(days=days),
        supersedes=previous,
    )
    VerificationCurrent.objects.update_or_create(
        entry=entry,
        field_group=field_group,
        level=level,
        defaults=dict(
            state="verified",
            verified_at=now,
            expires_at=event.expires_at,
            method=method,
            actor_display=(getattr(actor, "username", "") or "")[:80],
        ),
    )
    entry.last_verified_at = now
    entry.save(update_fields=["last_verified_at"])
    if field_group == "certificates" and level in ("surveyor", "ai"):
        entry.identifier_set.update(last_checked=now.date())
    if level in ("surveyor", "owner"):
        _mark_credit_eligible(entry)
    audit(
        "verification.record",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"level": level, "group": field_group},
    )
    try_publish(entry, actor=actor, now=now)
    return event


def _mark_credit_eligible(entry):
    """R09: payout credit needs a surveyor or owner check. Self-listed and agent-made entries never earn."""
    if entry.created_via in (Entry.CreatedVia.SELF, Entry.CreatedVia.AGENT):
        CreditEvent.objects.filter(entry=entry, kind="added").update(
            eligible=False, ineligible_reason=entry.created_via
        )
        return
    CreditEvent.objects.filter(entry=entry, kind="added", eligible=False, ineligible_reason="unverified").update(
        eligible=True, ineligible_reason=""
    )


@transaction.atomic
def revoke_verification(entry, *, field_group, level, actor, reason):
    previous = (
        VerificationEvent.objects.filter(entry=entry, field_group=field_group, level=level).order_by("-id").first()
    )
    VerificationEvent.objects.create(
        entry=entry,
        country_code=entry.country_code,
        field_group=field_group,
        level=level,
        state="revoked",
        actor_id=getattr(actor, "pk", None),
        evidence_text=reason,
        supersedes=previous,
    )
    VerificationCurrent.objects.filter(entry=entry, field_group=field_group, level=level).update(state="revoked")
    audit(
        "verification.revoke",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"level": level, "group": field_group, "reason": reason},
    )


@transaction.atomic
def sweep_expired(now=None):
    """Drop expired checks; return published entries that lost every check past the grace period to draft (R07, R08)."""
    now = now or clock.now()
    expired = list(VerificationCurrent.objects.select_for_update().filter(state="verified", expires_at__lte=now))
    touched = set()
    for cur in expired:
        previous = (
            VerificationEvent.objects.filter(entry_id=cur.entry_id, field_group=cur.field_group, level=cur.level)
            .order_by("-id")
            .first()
        )
        VerificationEvent.objects.create(
            entry_id=cur.entry_id,
            country_code=cur.entry.country_code,
            field_group=cur.field_group,
            level=cur.level,
            state="expired",
            ts=now,
            supersedes=previous,
        )
        cur.state = "expired"
        cur.save(update_fields=["state"])
        touched.add(cur.entry_id)
    returned = 0
    grace = timedelta(days=settings.GRACE_DAYS)
    for entry in Entry.objects.filter(publish_state=Entry.PublishState.PUBLISHED):
        if current_level(entry, now) != "none":
            continue
        last_expiry = max((v.expires_at for v in entry.verification_current.all() if v.expires_at), default=None)
        if last_expiry is None or now > last_expiry + grace:
            entry.publish_state = Entry.PublishState.DRAFT
            entry.save(update_fields=["publish_state"])
            audit(
                "entry.to_draft",
                object_type="entry",
                object_uid=entry.uid,
                country_code=entry.country_code,
                payload={"reason": "checks expired past grace"},
            )
            returned += 1
    return {"expired": len(expired), "returned_to_draft": returned}


# ---- publish bar ---------------------------------------------------------------------------------------------


def quality_failures(entry, now=None):
    """Why an entry may not be public yet (plan 6.1). Empty list means it clears the bar."""
    fails = []
    if not entry.name.strip():
        fails.append("name missing")
    if not entry.place_id:
        fails.append("place missing")
    if current_level(entry, now) == "none":
        fails.append("needs at least an AI check")
    if not (entry.website or entry.contact_set.exists()):
        fails.append("needs a website or a contact")
    if entry.source_id:
        try:
            assert_allowed(entry.source, "display")
        except SourceBlocked as exc:
            fails.append(str(exc))
    switch = CountrySwitch.for_country(entry.country_code)
    cs = ListTypeSettings.objects.filter(concept_id=entry.primary_concept_id).first()
    if entry.entity_type == Entry.EntityType.PERSON:
        if not switch.named_individuals_on:
            fails.append("named individuals are off in this country")
        latest = entry.consents.order_by("-id").first()
        if not latest or latest.status != "consented":
            fails.append("person needs recorded consent")
    if cs and cs.is_child_facing and not switch.child_services_on:
        fails.append("child-facing services are off in this country")
    tpl = entry.primary_concept.template
    if tpl:
        for key, msg in validate_addons(tpl, entry.addons, for_publish=True):
            fails.append(f"{key}: {msg}")
    return fails


def try_publish(entry, *, actor=None, now=None):
    """Move draft or review to published when the bar is met. Returns the failure list (empty if published)."""
    if entry.publish_state not in (Entry.PublishState.DRAFT, Entry.PublishState.REVIEW):
        return []
    fails = quality_failures(entry, now)
    if not fails:
        entry.publish_state = Entry.PublishState.PUBLISHED
        entry.save(update_fields=["publish_state"])
        from ledger.services import lock_phase  # late import: the ledger reads entries

        lock_phase(entry)
        audit("entry.publish", actor=actor, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return fails


# ---- claims and consent --------------------------------------------------------------------------------------


@transaction.atomic
def start_claim(entry, user, method, evidence=""):
    if entry.claim_state == Entry.ClaimState.CLAIMED:
        raise EntryError("entry is already claimed")
    claim = Claim.objects.create(entry=entry, user=user, method=method, evidence_text=evidence)
    entry.claim_state = Entry.ClaimState.PENDING
    entry.save(update_fields=["claim_state"])
    audit("claim.start", actor=user, object_type="entry", object_uid=entry.uid, country_code=entry.country_code)
    return claim


@transaction.atomic
def decide_claim(claim, *, actor, approve, now=None):
    now = now or clock.now()
    if claim.state != Claim.State.PENDING:
        raise EntryError("claim already decided")
    claim.state = Claim.State.APPROVED if approve else Claim.State.REJECTED
    claim.decided_by_id, claim.decided_at = actor.pk, now
    claim.save()
    entry = claim.entry
    entry.claim_state = Entry.ClaimState.CLAIMED if approve else Entry.ClaimState.UNCLAIMED
    entry.save(update_fields=["claim_state"])
    audit(
        "claim.decide",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"approved": approve},
    )
    if approve:
        record_verification(
            entry,
            field_group="identity",
            level="owner",
            actor=claim.user,
            method=claim.method,
            evidence=claim.evidence_text or "claim approved",
            now=now,
        )
    return claim


def record_consent(entry, *, status, method, wording_version, evidence="", actor=None):
    rec = ConsentRecord.objects.create(
        entry=entry, status=status, method=method, wording_version=wording_version, evidence_text=evidence
    )
    audit(
        "consent.record",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"status": status},
    )
    return rec


# ---- merging (plan 6.7, rule D6) -----------------------------------------------------------------------------


@transaction.atomic
def merge_entries(keep, drop, *, actor=None, score=None):
    """Merge `drop` into `keep`. Children move, credit events are re-pointed, the earliest added-credit survives,
    the dropped entry is tombstoned with a redirect, and everything is logged."""
    from .models import MergeMap

    if keep.pk == drop.pk or drop.merged_into_id:
        raise EntryError("cannot merge an entry into itself or merge twice")
    if keep.country_code != drop.country_code:
        raise EntryError("entries in different countries are never merged")
    for rel in (
        "namevariant_set",
        "contact_set",
        "social_set",
        "hours_set",
        "service_set",
        "product_set",
        "speciality_set",
        "identifier_set",
        "areaserved_set",
        "equipment_set",
        "branch_set",
    ):
        getattr(drop, rel).update(entry=keep)
    NameVariant.objects.get_or_create(
        entry=keep,
        country_code=keep.country_code,
        text=drop.name,
        defaults=dict(language=drop.name_lang, kind="old", text_fold=drop.name_fold),
    )
    CreditEvent.objects.filter(entry=drop).update(entry=keep, merged_from_id=drop.pk)
    added = list(CreditEvent.objects.filter(entry=keep, kind="added").order_by("created_at", "id"))
    for later in added[1:]:
        later.eligible, later.ineligible_reason = False, "duplicate"
        later.save(update_fields=["eligible", "ineligible_reason"])
    drop.merged_into = keep
    drop.publish_state = Entry.PublishState.SUPPRESSED
    drop.save(update_fields=["merged_into", "publish_state"])
    MergeMap.objects.create(from_entry=drop, to_entry=keep, score=score, decided_by_id=getattr(actor, "pk", None))
    ChangeLog.objects.create(
        entry_id=keep.pk,
        country_code=keep.country_code,
        field_key="merged",
        new={"from": drop.uid},
        actor_id=getattr(actor, "pk", None),
    )
    audit(
        "entry.merge",
        actor=actor,
        object_type="entry",
        object_uid=keep.uid,
        country_code=keep.country_code,
        payload={"from": drop.uid, "score": score},
    )
    return keep


@transaction.atomic
def approve_claim_by_code(claim, contact, *, wording_version="v1"):
    """A claimant who proved control of a stored contact with a one-time code becomes the owner. The decision is recorded
    against the claimant, with the method, so a moderator can review it later."""
    from outreach.services import record_optin

    start = claim.entry
    decide_claim(claim, actor=claim.user, approve=True)
    record_optin(
        contact, method="claim_otp", wording_version=wording_version, evidence=f"code verified for {start.uid}"
    )
    return claim


# ---- company page (plan 8.3.3) ---------------------------------------------------------------------------------

COMPANY_KINDS = ("about", "products", "capacity", "terms", "faq")


def company_page_active(entry, today=None):
    from core import clock as _clock

    today = today or _clock.today()
    return entry.listing_plan == "company" and (entry.plan_valid_until is None or entry.plan_valid_until >= today)


def company_page_allowed(entry):
    """Individuals and child-facing services are not eligible (R18, R19)."""
    cs = ListTypeSettings.objects.filter(concept_id=entry.primary_concept_id).first()
    return entry.entity_type != Entry.EntityType.PERSON and not (cs and cs.is_child_facing)


@transaction.atomic
def activate_company_plan(entry, *, days, actor=None):
    from datetime import timedelta as _td

    from core import clock as _clock

    if not company_page_allowed(entry):
        raise EntryError("this entry is not eligible for a company page")
    entry.listing_plan = "company"
    base = max(entry.plan_valid_until or _clock.today(), _clock.today())
    entry.plan_valid_until = base + _td(days=days)
    entry.save(update_fields=["listing_plan", "plan_valid_until"])
    audit(
        "plan.activate",
        actor=actor,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"plan": "company", "until": entry.plan_valid_until.isoformat()},
    )
    return entry


def is_owner(entry, user):
    return bool(
        getattr(user, "is_authenticated", False)
        and entry.claim_state == Entry.ClaimState.CLAIMED
        and Claim.objects.filter(entry=entry, user=user, state=Claim.State.APPROVED).exists()
    )


@transaction.atomic
def save_company_section(entry, user, kind, body, *, title="", section_id=None):
    """Owners write sections; each save goes back to pending until a moderator approves it."""
    from .models import CompanySection

    if not is_owner(entry, user):
        raise GuardError("only the owner can edit the company page")
    if not company_page_active(entry):
        raise GuardError("the company page plan is not active")
    if kind not in COMPANY_KINDS:
        raise EntryError("unknown section")
    body = (body or "").strip()
    if not body:
        raise EntryError("write something first")
    for banned in ("http://", "https://", "www."):
        if banned in body.lower() and kind != "products":
            raise EntryError("links are not allowed in this section")
    if section_id:
        sec = CompanySection.objects.get(pk=section_id, entry=entry)
        sec.title, sec.body, sec.state = title[:160], body[:4000], CompanySection.State.PENDING
        sec.updated_at = clock.now()
        sec.save()
    else:
        sec = CompanySection.objects.create(entry=entry, kind=kind, title=title[:160], body=body[:4000])
    audit(
        "company.section_saved",
        actor=user,
        object_type="entry",
        object_uid=entry.uid,
        country_code=entry.country_code,
        payload={"kind": kind},
    )
    return sec


@transaction.atomic
def moderate_company_section(section, *, actor, approve):
    section.state = "approved" if approve else "rejected"
    section.moderated_by_id = actor.pk
    section.save(update_fields=["state", "moderated_by_id"])
    audit(
        "company.section_moderated",
        actor=actor,
        object_type="entry",
        object_uid=section.entry.uid,
        country_code=section.entry.country_code,
        payload={"approved": approve, "kind": section.kind},
    )
    return section
