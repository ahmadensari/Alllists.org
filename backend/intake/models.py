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


class ImportBatch(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded"
        MAPPED = "mapped"
        DONE = "done"
        FAILED = "failed"

    source = models.ForeignKey(Source, on_delete=models.PROTECT, related_name="batches")
    uploader = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL, related_name="+")
    declared_rights = models.BooleanField(default=False)  # contributor declares the right to share (D11)
    place = models.ForeignKey("places.Place", on_delete=models.PROTECT, related_name="+")
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.PROTECT, related_name="+")
    raw_text = models.TextField()
    mapping = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.UPLOADED)
    counts = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)


class ImportRow(models.Model):
    class Status(models.TextChoices):
        NEW = "new"
        DUPLICATE = "duplicate"
        HELD = "held"
        ERROR = "error"
        DRAFTED = "drafted"

    batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE, related_name="rows")
    line_no = models.PositiveIntegerField()
    raw = models.JSONField(default=dict)
    normalised = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
    message = models.CharField(max_length=200, blank=True)
    entry = models.ForeignKey("entries.Entry", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")


class DedupeCandidate(models.Model):
    class State(models.TextChoices):
        PENDING = "pending"
        AUTO_MERGED = "auto_merged"
        REJECTED = "rejected"
        MERGED = "merged"

    a_entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="+")
    b_entry = models.ForeignKey("entries.Entry", on_delete=models.CASCADE, related_name="+")
    score = models.FloatField()
    features = models.JSONField(default=dict)
    state = models.CharField(max_length=12, choices=State.choices, default=State.PENDING)
    decided_by_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["a_entry", "b_entry"], name="uniq_dedupe_pair")]
