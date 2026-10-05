"""Source register (plan section 7.1). Every import and agent fetch references a source; the gate decides."""
from django.db import models


class Source(models.Model):
    class Tier(models.TextChoices):
        GREEN = "green"
        AMBER = "amber"
        RED = "red"

    name = models.CharField(max_length=160, unique=True)
    tier = models.CharField(max_length=6, choices=Tier.choices, default=Tier.AMBER)
    licence_text = models.TextField(blank=True)
    terms_url = models.URLField(blank=True)
    robots_decision = models.CharField(max_length=60, blank=True)
    allowed_uses = models.JSONField(default=list, blank=True)  # e.g. ["import", "agent_fetch", "display"]
    bulk_permission = models.BooleanField(default=False)
    personal_data_rules = models.TextField(blank=True)
    attribution_text = models.CharField(max_length=300, blank=True)
    reviewed_by = models.CharField(max_length=120, blank=True)
    reviewed_on = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, default="active")

    def __str__(self):
        return self.name
