import pytest
from django.db import connection, transaction
from django.db.utils import IntegrityError, InternalError

from core import clock
from core.crypto import CryptoError, decrypt, encrypt, keyed_hash
from core.models import AuditLog, ChangeLog, audit, verify_audit_chain
from core.textfold import fold
from core.ulid import new_ulid


def test_ulid_is_26_chars_unique_and_time_ordered():
    a, b = new_ulid(1000), new_ulid(2000)
    assert len(a) == 26 and a < b and new_ulid() != new_ulid()


@pytest.mark.parametrize("a,b", [
    ("کراچی", "کراچی"),
    ("ياسر", "یاسر"),          # Arabic yeh vs Farsi yeh
    ("كراچی", "کراچی"),  # Arabic kaf vs keheh
    ("آمین", "امین"),                                                   # madda folds to alef
    ("پاکستان‌", "پاکستان"),
    ("سیالکوٹ ١٢٣", "سیالکوٹ 123"),                                     # Arabic-Indic digits
    ("Paris  Road!", "paris road"),
    ("ہوٹل", "ہوٹل"),
])
def test_fold_unifies_variants(a, b):
    assert fold(a) == fold(b)


def test_fold_removes_marks_and_tatweel():
    assert fold("مُحَمَّد") == fold("محمد")
    assert fold("اللـه") == fold("الله")
    assert fold("") == "" and fold(None) == ""


def test_zwnj_becomes_space():
    assert fold("ہوٹل‌سٹی") == "ہوٹل سٹی"


def test_encrypt_roundtrip_and_key_rotation(settings):
    from cryptography.fernet import Fernet
    token = encrypt("+923001234567")
    assert token.startswith("dev:") and "923001234567" not in token and decrypt(token) == "+923001234567"
    settings.FIELD_ENCRYPTION_KEYS = {**settings.FIELD_ENCRYPTION_KEYS, "k2": Fernet.generate_key().decode()}
    settings.FIELD_ENCRYPTION_ACTIVE_KEY = "k2"
    assert encrypt("x").startswith("k2:") and decrypt(token) == "+923001234567"
    with pytest.raises(CryptoError):
        decrypt("nokey:abc")


def test_keyed_hash_is_stable_and_keyed(settings):
    h1 = keyed_hash("phone:+923001234567")
    assert h1 == keyed_hash("phone:+923001234567") and len(h1) == 64
    settings.CONTACT_HASH_PEPPER = "other"
    assert keyed_hash("phone:+923001234567") != h1


@pytest.mark.django_db
def test_audit_chain_verifies_and_links():
    a = audit("t.one")
    b = audit("t.two", payload={"k": 1})
    assert b.prev_hash == a.hash and verify_audit_chain() is None


def test_audit_chain_detects_tamper(pg):
    audit("t.one")
    row = audit("t.two", payload={"k": 1})
    with connection.cursor() as cur:
        cur.execute("ALTER TABLE core_auditlog DISABLE TRIGGER core_auditlog_append_only")
        cur.execute("UPDATE core_auditlog SET payload = '{\"k\": 2}' WHERE id = %s", [row.id])
        cur.execute("ALTER TABLE core_auditlog ENABLE TRIGGER core_auditlog_append_only")
    assert verify_audit_chain() == row.id


@pytest.mark.parametrize("model", [AuditLog, ChangeLog])
def test_append_only_tables_refuse_update_and_delete(pg, model):
    if model is AuditLog:
        obj = audit("t.one")
    else:
        obj = ChangeLog.objects.create(entry_id=1, country_code="PK", field_key="name", new="x")
    for sql in (f"UPDATE {model._meta.db_table} SET country_code = 'AE'", f"DELETE FROM {model._meta.db_table}"):
        with pytest.raises((InternalError, IntegrityError)), transaction.atomic():
            with connection.cursor() as cur:
                cur.execute(sql)
    assert model.objects.filter(pk=obj.pk).exists()


def test_clock_override():
    import datetime
    from django.utils import timezone
    fixed = timezone.make_aware(datetime.datetime(2026, 1, 2, 3, 4))
    clock.set_now(fixed)
    try:
        assert clock.now() == fixed
    finally:
        clock.set_now(None)


def test_seed_pilot_is_idempotent_and_safe_by_default(db):
    from django.core.management import call_command
    from core.models import CountrySwitch
    from places.models import Place
    from taxonomy.models import Concept
    call_command("seed_pilot")
    call_command("seed_pilot")
    assert Place.objects.filter(path="pk.punjab.sialkot").count() == 1
    assert Place.objects.filter(parent__path="pk.punjab.sialkot").count() == 3
    assert Concept.objects.filter(slug="surgical-instrument-makers").count() == 1
    sw = CountrySwitch.objects.get(country_code="PK")
    assert sw.browsing_on and not (sw.selling_on or sw.outreach_on or sw.indexing_on or sw.named_individuals_on)
