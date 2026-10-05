"""Shared base models: ids, soft delete, audit hash chain, change log, flags, country switches (plan section 4.2.1)."""

import hashlib
import json

from django.conf import settings
from django.db import connection, models, transaction

from . import clock
from .ulid import new_ulid


class UidModel(models.Model):
    uid = models.CharField(max_length=26, unique=True, default=new_ulid, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    tombstone_reason = models.CharField(max_length=80, blank=True)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """Append-only, hash-chained: hash = sha256(prev_hash + canonical row). Written in the same transaction as the change."""

    ts = models.DateTimeField()
    actor_id = models.BigIntegerField(null=True, blank=True)
    actor_role = models.CharField(max_length=40, blank=True)
    action = models.CharField(max_length=80)
    object_type = models.CharField(max_length=60, blank=True)
    object_uid = models.CharField(max_length=40, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    ip_hash = models.CharField(max_length=64, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    prev_hash = models.CharField(max_length=64, blank=True)
    hash = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ["id"]


def _canonical(prev_hash, fields):
    return prev_hash + json.dumps(fields, sort_keys=True, separators=(",", ":"), default=str)


def audit(
    action, *, actor=None, actor_role="", object_type="", object_uid="", country_code="", ip_hash="", payload=None
):
    """Append one audit row. Call inside the transaction that makes the change."""
    with transaction.atomic():
        if connection.vendor == "postgresql":
            with connection.cursor() as cur:
                cur.execute("SELECT pg_advisory_xact_lock(727001)")
        last = AuditLog.objects.order_by("-id").first()
        prev = last.hash if last else ""
        ts = clock.now()
        fields = {
            "ts": ts.isoformat(),
            "actor_id": getattr(actor, "pk", actor),
            "actor_role": actor_role,
            "action": action,
            "object_type": object_type,
            "object_uid": object_uid,
            "country_code": country_code,
            "ip_hash": ip_hash,
            "payload": payload or {},
        }
        digest = hashlib.sha256(_canonical(prev, fields).encode()).hexdigest()
        return AuditLog.objects.create(
            ts=ts,
            actor_id=fields["actor_id"],
            actor_role=actor_role,
            action=action,
            object_type=object_type,
            object_uid=object_uid,
            country_code=country_code,
            ip_hash=ip_hash,
            payload=fields["payload"],
            prev_hash=prev,
            hash=digest,
        )


def verify_audit_chain():
    """Returns None if the chain is intact, else the id of the first broken row."""
    prev = ""
    for row in AuditLog.objects.order_by("id").iterator():
        fields = {
            "ts": row.ts.isoformat(),
            "actor_id": row.actor_id,
            "actor_role": row.actor_role,
            "action": row.action,
            "object_type": row.object_type,
            "object_uid": row.object_uid,
            "country_code": row.country_code,
            "ip_hash": row.ip_hash,
            "payload": row.payload,
        }
        if row.prev_hash != prev or hashlib.sha256(_canonical(prev, fields).encode()).hexdigest() != row.hash:
            return row.id
        prev = row.hash
    return None


class ChangeLog(models.Model):
    """One row per field change on an entry (append-only)."""

    entry_id = models.BigIntegerField(db_index=True)
    country_code = models.CharField(max_length=2)
    field_key = models.CharField(max_length=60)
    old = models.JSONField(null=True, blank=True)
    new = models.JSONField(null=True, blank=True)
    actor_id = models.BigIntegerField(null=True, blank=True)
    source_id = models.BigIntegerField(null=True, blank=True)
    ts = models.DateTimeField(default=clock.now)

    class Meta:
        ordering = ["id"]


class FeatureFlag(models.Model):
    key = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=200, blank=True)
    enabled_default = models.BooleanField(default=False)
    country_code = models.CharField(max_length=2, blank=True, help_text="Blank means every country")
    rollout_percent = models.PositiveSmallIntegerField(default=100)


class CountrySwitch(models.Model):
    """Per-country control for rule R24. Everything except browsing defaults to off."""

    country_code = models.CharField(max_length=2, unique=True)
    browsing_on = models.BooleanField(default=True)
    indexing_on = models.BooleanField(default=False)
    selling_on = models.BooleanField(default=False)
    outreach_on = models.BooleanField(default=False)
    outreach_channels = models.JSONField(default=list, blank=True)
    ads_on = models.BooleanField(default=False)
    named_individuals_on = models.BooleanField(default=False)
    health_prices_on = models.BooleanField(default=False)
    child_services_on = models.BooleanField(default=False)
    publish_cap_per_week = models.PositiveIntegerField(default=0)
    legal_note = models.TextField(blank=True)
    cleared_by = models.CharField(max_length=120, blank=True)
    cleared_on = models.DateField(null=True, blank=True)

    @classmethod
    def for_country(cls, code):
        """Unknown countries get the all-off default (browsing only)."""
        return cls.objects.filter(country_code=code).first() or cls(country_code=code)


class RegistryVersion(models.Model):
    registry_key = models.CharField(max_length=60)
    version = models.PositiveIntegerField()
    changed_at = models.DateTimeField(default=clock.now)
    changed_by = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = [("registry_key", "version")]


def flag_enabled(key, country_code=""):
    f = FeatureFlag.objects.filter(key=key, country_code__in=[country_code, ""]).order_by("-country_code").first()
    return bool(f and f.enabled_default and f.rollout_percent > 0)


AUTH_USER = settings.AUTH_USER_MODEL


class JobRun(models.Model):
    """Last run of each scheduled job (plan appendix F). Lets a simple scheduler decide what is due."""

    name = models.CharField(max_length=60, unique=True)
    last_run = models.DateTimeField(null=True, blank=True)
    last_result = models.CharField(max_length=200, blank=True)
    last_error = models.CharField(max_length=300, blank=True)
