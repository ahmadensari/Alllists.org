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
    from django.db.models import TextField
    from django.db.models.functions import Cast

    active = settings.FIELD_ENCRYPTION_ACTIVE_KEY + ":"
    changed = 0
    for model in apps.get_models():
        names = [f.name for f in model._meta.get_fields() if isinstance(f, EncryptedTextField)]
        if not names:
            continue
        # the cast reads the stored text itself (key id and ciphertext) instead of the decrypted value
        qs = model._default_manager.annotate(**{f"_raw_{n}": Cast(n, TextField()) for n in names})
        for obj in qs.iterator(chunk_size=batch):
            stale = [n for n in names if getattr(obj, f"_raw_{n}") and not getattr(obj, f"_raw_{n}").startswith(active)]
            if stale:
                model._default_manager.filter(pk=obj.pk).update(**{n: getattr(obj, n) for n in stale})
                changed += len(stale)
    return changed
