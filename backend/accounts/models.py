"""Accounts, roles, MFA, login throttling (plan section 11)."""

from django.conf import settings
from django.db import models

from core import clock
from core.crypto import EncryptedTextField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=60, blank=True)  # chosen public name; never the real name by default
    lang = models.CharField(max_length=2, default="en")
    saved_place_uid = models.CharField(max_length=26, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=clock.now)

    def public_name(self):
        return self.display_name or f"user-{self.user_id}"


class EmailToken(models.Model):
    """Single-use token for email verification. Only the hash is stored."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    token_hash = models.CharField(max_length=64, unique=True)
    purpose = models.CharField(max_length=20, default="verify")
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)


class LoginAttempt(models.Model):
    key_hash = models.CharField(max_length=64, db_index=True)  # keyed hash of account name or address
    kind = models.CharField(max_length=8)  # account | address
    ts = models.DateTimeField(default=clock.now, db_index=True)
    success = models.BooleanField(default=False)


class TOTPDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="totp")
    secret_enc = EncryptedTextField()
    confirmed = models.BooleanField(default=False)
    last_step = models.BigIntegerField(default=0)  # blocks replay of the same code
    created_at = models.DateTimeField(default=clock.now)


class RecoveryCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    code_hash = models.CharField(max_length=64)
    used_at = models.DateTimeField(null=True, blank=True)


class SocialIdentity(models.Model):
    """A sign-in at an outside provider (Google, ORCID) linked to one account. The provider's subject is the key."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="social_identities")
    provider = models.CharField(max_length=20)
    subject = models.CharField(max_length=120)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["provider", "subject"], name="uniq_social_subject")]
