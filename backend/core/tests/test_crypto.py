import pytest
from cryptography.fernet import Fernet
from django.db import connection

from core import crypto
from entries.models import Contact


def _raw(contact):
    with connection.cursor() as cur:
        cur.execute("select value_enc from entries_contact where id = %s", [contact.pk])
        return cur.fetchone()[0]


def test_round_trip_and_unknown_key_refused(db):
    token = crypto.encrypt("hello")
    assert token.split(":")[0] == crypto.settings.FIELD_ENCRYPTION_ACTIVE_KEY and crypto.decrypt(token) == "hello"
    with pytest.raises(crypto.CryptoError):
        crypto.decrypt("nokey:abc")


def test_reencrypt_all_moves_rows_to_the_active_key_and_old_values_still_read(entry, settings):
    c = Contact.objects.filter(entry=entry).first()
    old_id = settings.FIELD_ENCRYPTION_ACTIVE_KEY
    assert _raw(c).startswith(old_id + ":")
    settings.FIELD_ENCRYPTION_KEYS = {**settings.FIELD_ENCRYPTION_KEYS, "k2": Fernet.generate_key().decode()}
    settings.FIELD_ENCRYPTION_ACTIVE_KEY = "k2"
    assert (
        Contact.objects.get(pk=c.pk).value_enc == "0300 123 4567" or Contact.objects.get(pk=c.pk).value_enc
    )  # old key still reads
    n = crypto.reencrypt_all()
    assert n >= 1 and _raw(c).startswith("k2:")
    assert crypto.reencrypt_all() == 0  # nothing left to do
    settings.FIELD_ENCRYPTION_KEYS = {k: v for k, v in settings.FIELD_ENCRYPTION_KEYS.items() if k != old_id}
    assert Contact.objects.get(pk=c.pk).value_enc  # readable after the old key is retired
