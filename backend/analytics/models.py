from django.db import models

from core import clock


class RollupCell(models.Model):
    """Counts for one (place, concept) cell, including everything below the place. Only non-empty cells exist."""

    country_code = models.CharField(max_length=2)
    place_path = models.CharField(max_length=500)
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.CASCADE, related_name="+")
    total = models.PositiveIntegerField(default=0)
    published = models.PositiveIntegerField(default=0)
    by_level = models.JSONField(default=dict)
    verified_12m = models.PositiveIntegerField(default=0)
    with_contact_pct = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["country_code", "place_path", "concept"], name="uniq_rollup_cell")
        ]
        indexes = [models.Index(fields=["country_code", "place_path"], name="rollup_place_idx")]


class Event(models.Model):
    """Privacy-respecting server-side event (plan appendix G): hashed subject, no contact values."""

    name = models.CharField(max_length=40, db_index=True)
    ts = models.DateTimeField(default=clock.now, db_index=True)
    subject_hash = models.CharField(max_length=64, blank=True)
    props = models.JSONField(default=dict, blank=True)
