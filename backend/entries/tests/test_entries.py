from datetime import timedelta

import pytest
from django.db import connection, transaction
from django.db.utils import IntegrityError, InternalError

from core import clock
from core.models import ChangeLog, CountrySwitch, verify_audit_chain
from entries import services as es
from entries.models import Contact, CreditEvent, VerificationCurrent, VerificationEvent
from intake.gate import SourceBlocked
from intake.models import Source
from taxonomy.models import ListTypeSettings


def verify(entry, user, level="surveyor", **kw):
    return es.record_verification(
        entry, field_group="identity", level=level, actor=user, method=kw.pop("method", "call"),
        evidence=kw.pop("evidence", "Phone answered, name matched"), **kw)


# ---- creation, contacts, history (R02, R21) ------------------------------------------------------------------

def test_create_is_draft_with_country_path_and_template_version(entry, tree):
    assert entry.publish_state == "draft" and entry.country_code == "PK"
    assert entry.place_path == tree["paris"].path and entry.addon_template_version == 1
    assert ChangeLog.objects.filter(entry_id=entry.pk, field_key="created").exists()
    assert verify_audit_chain() is None


def test_contact_is_encrypted_at_rest_and_hashed(pg, entry):
    c = Contact.objects.get(entry=entry)
    with connection.cursor() as cur:
        cur.execute("SELECT value_enc FROM entries_contact WHERE id=%s", [c.pk])
        raw = cur.fetchone()[0]
    assert "923001234567" not in raw and raw.startswith("dev:")
    assert c.value_enc == "+923001234567" and c.relay_only is True
    assert Contact.objects.filter(value_hash=c.value_hash).count() == 1


def test_contact_normalisation_and_same_number_same_hash(entry):
    es.add_contact(entry, "phone", "+92 (300) 123-4567")
    assert Contact.objects.filter(entry=entry).values("value_hash").distinct().count() == 1
    assert es.normalize_contact("email", " A@B.CO ") == "a@b.co"


def test_invalid_addons_rejected(tree, surgical, users):
    with pytest.raises(es.EntryError):
        es.create_entry(name="X", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        addons={"business_type": "pirate"})


def test_update_writes_change_log_and_refolds_name(entry, users):
    es.update_entry(entry, actor=users["mod"], name="كريسنت Surgical", website="https://new.example.org")
    rows = {r.field_key: r for r in ChangeLog.objects.filter(entry_id=entry.pk)}
    assert rows["website"].old == "https://example.org" and rows["name"].new == "كريسنت Surgical"
    entry.refresh_from_db()
    assert "ک" in entry.name_fold
    with pytest.raises(es.EntryError):
        es.update_entry(entry, publish_state="published")


def test_import_needs_an_allowed_source(tree, surgical, users, db):
    red = Source.objects.create(name="Scraped maps", tier="red", allowed_uses=["import"])
    with pytest.raises(SourceBlocked):
        es.create_entry(name="X", place=tree["paris"], primary_concept=surgical, created_via="import", source=red,
                        addons={"business_type": "trader", "product_categories": ["a"]})
    with pytest.raises(SourceBlocked):
        es.create_entry(name="X", place=tree["paris"], primary_concept=surgical, created_via="import", source=None)


# ---- verification guards (R07) -------------------------------------------------------------------------------

def test_surveyor_never_verifies_own_entry(entry, users):
    with pytest.raises(es.GuardError):
        verify(entry, users["adder"])
    assert verify(entry, users["surveyor"]).state == "verified"


def test_surveyor_and_owner_need_method_and_evidence(entry, users):
    with pytest.raises(es.GuardError):
        verify(entry, users["surveyor"], evidence="  ")
    with pytest.raises(es.GuardError):
        verify(entry, users["surveyor"], method="")
    with pytest.raises(es.GuardError):
        es.record_verification(entry, field_group="identity", level="surveyor", actor=None, method="call", evidence="x")


def test_owner_check_needs_approved_claim(entry, users):
    with pytest.raises(es.GuardError):
        verify(entry, users["owner"], level="owner")
    claim = es.start_claim(entry, users["owner"], "otp_phone", "OTP matched stored phone")
    with pytest.raises(es.GuardError):
        verify(entry, users["owner"], level="owner")
    es.decide_claim(claim, actor=users["mod"], approve=True)
    entry.refresh_from_db()
    assert entry.claim_state == "claimed" and es.current_level(entry) == "owner"


def test_rejected_claim_leaves_entry_unclaimed(entry, users):
    claim = es.start_claim(entry, users["owner"], "otp_phone")
    es.decide_claim(claim, actor=users["mod"], approve=False)
    entry.refresh_from_db()
    assert entry.claim_state == "unclaimed"
    with pytest.raises(es.EntryError):
        es.decide_claim(claim, actor=users["mod"], approve=True)


def test_ai_check_needs_different_source_and_evidence(entry, users, green, web_source):
    es.update_entry(entry)  # no-op
    entry.source = green
    entry.save()
    with pytest.raises(es.GuardError):
        es.record_verification(entry, field_group="identity", level="ai", source=green, evidence="same", method="web")
    with pytest.raises(es.GuardError):
        es.record_verification(entry, field_group="identity", level="ai", source=None, evidence="x", method="web")
    with pytest.raises(es.GuardError):
        es.record_verification(entry, field_group="identity", level="ai", source=web_source, evidence="", method="web")
    ev = es.record_verification(entry, field_group="identity", level="ai", source=web_source,
                                evidence="Page lists the same address", method="web")
    assert ev.state == "verified"


def test_ai_check_refuses_red_or_unreviewed_source(entry):
    red = Source.objects.create(name="Bought list", tier="red", allowed_uses=["agent_fetch"])
    with pytest.raises(SourceBlocked):
        es.record_verification(entry, field_group="identity", level="ai", source=red, evidence="x", method="web")


def test_levels_are_independent_chips(entry, users, web_source):
    verify(entry, users["surveyor"])
    es.record_verification(entry, field_group="identity", level="ai", source=web_source, evidence="e", method="web")
    assert es.current_levels(entry) == {"surveyor", "ai"} and es.current_level(entry) == "surveyor"


def test_reverification_supersedes_and_keeps_history(entry, users):
    e1 = verify(entry, users["surveyor"])
    e2 = verify(entry, users["surveyor"])
    assert e2.supersedes_id == e1.pk and VerificationEvent.objects.filter(entry=entry).count() == 2
    assert VerificationCurrent.objects.filter(entry=entry).count() == 1


def test_revoke(entry, users):
    verify(entry, users["surveyor"])
    es.revoke_verification(entry, field_group="identity", level="surveyor", actor=users["mod"], reason="report upheld")
    assert es.current_level(entry) == "none"


def test_append_only_verification_event(pg, entry, users):
    ev = verify(entry, users["surveyor"])
    with pytest.raises((InternalError, IntegrityError)), transaction.atomic():
        with connection.cursor() as cur:
            cur.execute("UPDATE entries_verificationevent SET method='x' WHERE id=%s", [ev.pk])


# ---- expiry and grace (R07, R08) -----------------------------------------------------------------------------

def test_checks_expire_then_grace_then_draft(entry, users, settings):
    t0 = clock.now()
    verify(entry, users["surveyor"], now=t0)
    entry.refresh_from_db()
    assert entry.publish_state == "published" and es.current_level(entry, t0) == "surveyor"
    after = t0 + timedelta(days=settings.CHECK_VALIDITY_DAYS["surveyor"] + 1)
    r = es.sweep_expired(after)
    entry.refresh_from_db()
    assert r == {"expired": 1, "returned_to_draft": 0} and entry.publish_state == "published"  # grace
    assert es.current_level(entry, after) == "none"
    later = after + timedelta(days=settings.GRACE_DAYS + 1)
    assert es.sweep_expired(later)["returned_to_draft"] == 1
    entry.refresh_from_db()
    assert entry.publish_state == "draft"
    assert VerificationEvent.objects.filter(entry=entry, state="expired").count() == 1


def test_ai_check_expires_sooner_than_surveyor(settings):
    assert settings.CHECK_VALIDITY_DAYS["ai"] < settings.CHECK_VALIDITY_DAYS["surveyor"]


# ---- publish bar (R08, R18, R19, R21) -------------------------------------------------------------------------

def test_draft_stays_draft_without_a_check(entry):
    assert entry.publish_state == "draft"
    assert "needs at least an AI check" in es.quality_failures(entry)


def test_needs_website_or_contact(tree, surgical, users):
    e = es.create_entry(name="No Contact Co", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        addons={"business_type": "trader", "product_categories": ["a"]})
    verify(e, users["surveyor"])
    e.refresh_from_db()
    assert e.publish_state == "draft" and "needs a website or a contact" in es.quality_failures(e)


def test_required_addon_fields_gate_publishing(tree, surgical, users):
    e = es.create_entry(name="Thin Co", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        website="https://t.example.org")
    verify(e, users["surveyor"])
    e.refresh_from_db()
    assert e.publish_state == "draft"
    fails = es.quality_failures(e)
    assert any(f.startswith("business_type") for f in fails)


def test_published_after_surveyor_check(entry, users):
    verify(entry, users["surveyor"])
    entry.refresh_from_db()
    assert entry.publish_state == "published"


def test_blocked_source_prevents_publish(entry, users, green):
    entry.source = green
    entry.save()
    green.status = "paused"
    green.save()
    verify(entry, users["surveyor"])
    entry.refresh_from_db()
    assert entry.publish_state == "draft" and any("not active" in f for f in es.quality_failures(entry))


def test_person_needs_switch_and_consent(tree, surgical, users, db):
    e = es.create_entry(name="Dr Example", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        entity_type="person", website="https://dr.example.org",
                        addons={"business_type": "trader", "product_categories": ["a"]})
    verify(e, users["surveyor"])
    e.refresh_from_db()
    assert e.publish_state == "draft"
    CountrySwitch.objects.create(country_code="PK", named_individuals_on=True)
    assert es.quality_failures(e) == ["person needs recorded consent"]
    es.record_consent(e, status="consented", method="signed form", wording_version="v1")
    assert es.try_publish(e) == [] and e.publish_state == "published"
    es.record_consent(e, status="withdrawn", method="email", wording_version="v1")
    e.publish_state = "draft"
    assert "person needs recorded consent" in es.quality_failures(e)


def test_child_facing_list_type_off_by_default(entry, users):
    ListTypeSettings.objects.filter(concept=entry.primary_concept).update(is_child_facing=True)
    verify(entry, users["surveyor"])
    entry.refresh_from_db()
    assert entry.publish_state == "draft"
    CountrySwitch.objects.create(country_code="PK", child_services_on=True)
    assert es.try_publish(entry) == []


def test_country_defaults_all_off_except_browsing(db):
    s = CountrySwitch.for_country("ZZ")
    assert s.browsing_on and not (s.indexing_on or s.selling_on or s.outreach_on or s.ads_on or s.named_individuals_on)


# ---- credit eligibility (R09, D6) -----------------------------------------------------------------------------

def test_credit_only_after_surveyor_or_owner_check(entry, users, web_source):
    ce = CreditEvent.objects.get(entry=entry)
    assert not ce.eligible and ce.ineligible_reason == "unverified"
    es.record_verification(entry, field_group="identity", level="ai", source=web_source, evidence="e", method="web")
    ce.refresh_from_db()
    assert not ce.eligible  # an AI check earns nothing
    verify(entry, users["surveyor"])
    ce.refresh_from_db()
    assert ce.eligible


def test_self_listed_never_earns(tree, surgical, users):
    e = es.create_entry(name="Self Listed", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        created_via="self", website="https://s.example.org",
                        addons={"business_type": "trader", "product_categories": ["a"]})
    verify(e, users["surveyor"])
    ce = CreditEvent.objects.get(entry=e)
    assert not ce.eligible and ce.ineligible_reason == "self"


def test_import_credit_waits_for_verification(tree, surgical, users, green):
    e = es.create_entry(name="Imported Co", place=tree["paris"], primary_concept=surgical, created_by=users["adder"],
                        created_via="import", source=green, website="https://i.example.org",
                        addons={"business_type": "trader", "product_categories": ["a"]})
    assert not CreditEvent.objects.get(entry=e).eligible
    verify(e, users["surveyor"])
    assert CreditEvent.objects.get(entry=e).eligible


def test_agent_entries_have_no_human_credit(tree, surgical, web_source):
    e = es.create_entry(name="Agent Draft", place=tree["paris"], primary_concept=surgical, created_via="agent",
                        source=web_source, addons={"business_type": "trader", "product_categories": ["a"]})
    assert not CreditEvent.objects.filter(entry=e).exists() and e.publish_state == "draft"
