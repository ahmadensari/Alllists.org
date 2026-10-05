"""Field encryption with key versioning, and keyed hashes for lookup without decryption (plan sections 4.1, 17)."""

import hashlib
import hmac

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models


class CryptoError(Exception):
    pass


def encrypt(plaintext: str) -> str:
    kid = settings.FIELD_ENCRYPTION_ACTIVE_KEY
    key = settings.FIELD_ENCRYPTION_KEYS.get(kid)
    if not key:
        raise CryptoError("no active encryption key configured")
    return f"{kid}:{Fernet(key.encode()).encrypt(plaintext.encode()).decode()}"


def decrypt(stored: str) -> str:
    kid, _, token = stored.partition(":")
    key = settings.FIELD_ENCRYPTION_KEYS.get(kid)
    if not key:
        raise CryptoError(f"unknown key id {kid!r}")
    try:
        return Fernet(key.encode()).decrypt(token.encode()).decode()
    except InvalidToken as exc:
        raise CryptoError("cannot decrypt value") from exc


def keyed_hash(value: str) -> str:
    """Stable keyed hash for de-duplication and suppression lists. Normalise before calling."""
    pepper = settings.CONTACT_HASH_PEPPER
    if not pepper:
        raise CryptoError("CONTACT_HASH_PEPPER is not set")
    return hmac.new(pepper.encode(), value.encode(), hashlib.sha256).hexdigest()


class EncryptedTextField(models.TextField):
    """Stores `key_id:ciphertext`. Never rendered to visitors (rule R02)."""

    def get_prep_value(self, value):
        if value is None:
            return None
        return encrypt(value)

    def from_db_value(self, value, expression, connection):
        return None if value is None else decrypt(value)


def reencrypt_all(batch=500):
    """Rewrite every encrypted value that is not under the active key (after a key rotation). Returns the number of
    values rewritten. Safe to run again; stop it and nothing is lost, rows are updated one at a time."""
    from django.apps import apps

    active = settings.FIELD_ENCRYPTION_ACTIVE_KEY + ":"
    changed = 0
    for model in apps.get_models():
        fields = [f for f in model._meta.get_fields() if isinstance(f, EncryptedTextField)]
        if not fields:
            continue
        names = [f.name for f in fields]
        for obj in model._default_manager.all().iterator(chunk_size=batch):
            stale = [n for n in names if getattr(obj, n) is not None and not _stored(obj, n).startswith(active)]
            if stale:
                # read the plaintext (already decrypted by the field) and write it back under the active key
                model._default_manager.filter(pk=obj.pk).update(**{n: getattr(obj, n) for n in stale})
                changed += len(stale)
    return changed


def _stored(obj, name):
    """The raw stored value of a field (its key id prefix), without decrypting."""
    model = type(obj)
    from django.db import connection

    q = connection.ops.quote_name
    col, table, pk = model._meta.get_field(name).column, model._meta.db_table, model._meta.pk.column
    with connection.cursor() as cur:
        # names come from Django's own model metadata and are quoted; the only value is bound
        cur.execute(f"select {q(col)} from {q(table)} where {q(pk)} = %s", [obj.pk])
        row = cur.fetchone()
    return row[0] if row and row[0] else ""
