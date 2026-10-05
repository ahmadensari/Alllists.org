"""Concepts (list types and more), labels, crosswalks, the add-on registry and list-type settings (plan sections 4.2.3, 5)."""
from django.db import models

from core import clock
from core.models import UidModel


class Concept(UidModel):
    class Kind(models.TextChoices):
        FAMILY = "family"
        LIST_TYPE = "list_type"
        SPECIALITY = "speciality"
        SERVICE = "service"
        PRODUCT = "product"

    class Scale(models.TextChoices):
        HYPER_LOCAL = "hyper_local"
        CITY = "city"
        NATIONAL = "national"
        GLOBAL = "global"

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="children")
    kind = models.CharField(max_length=12, choices=Kind.choices)
    slug = models.SlugField(max_length=120)
    entity_type_default = models.CharField(max_length=12, default="business")
    natural_scale = models.CharField(max_length=12, choices=Scale.choices, default=Scale.CITY)
    template = models.ForeignKey("AddonTemplate", null=True, blank=True, on_delete=models.SET_NULL, related_name="concepts")
    status = models.CharField(max_length=10, default="active")
    created_by_id = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["kind", "slug"], name="uniq_concept_slug_per_kind")]

    def __str__(self):
        return self.slug

    def label(self, language="en"):
        labels = list(self.labels.all())
        for lb in labels:
            if lb.language == language and lb.kind == ConceptLabel.Kind.PREFERRED:
                return lb.text
        for lb in labels:
            if lb.kind == ConceptLabel.Kind.PREFERRED:
                return lb.text
        return self.slug


class ConceptLabel(models.Model):
    class Kind(models.TextChoices):
        PREFERRED = "preferred"
        SYNONYM = "synonym"
        LOCAL = "local"
        MISSPELLING = "misspelling"

    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="labels")
    language = models.CharField(max_length=10)
    region = models.CharField(max_length=2, blank=True)
    kind = models.CharField(max_length=12, choices=Kind.choices, default=Kind.PREFERRED)
    text = models.CharField(max_length=200)
    text_fold = models.CharField(max_length=200, db_index=True)


class ConceptCrosswalk(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="crosswalks")
    system = models.CharField(max_length=20)  # isic, isco, overture, foursquare, osm, schema_org, hs
    code = models.CharField(max_length=80)
    match_type = models.CharField(max_length=10, default="exact")


class AddonTemplate(models.Model):
    key = models.SlugField(unique=True)
    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, default="active")
    description = models.CharField(max_length=200, blank=True)


class AddonField(models.Model):
    """Fields can be added or deprecated, never changed in meaning (spec rule 3)."""
    class Type(models.TextChoices):
        TEXT = "text"
        NUMBER = "number"
        ENUM = "enum"
        BOOL = "bool"
        DATE = "date"
        CONCEPT_LIST = "concept_list"
        MONEY = "money"
        IDENTIFIER_LIST = "identifier_list"
        PLACE_LIST = "place_list"

    class Show(models.TextChoices):
        PUBLIC = "P"
        LOCKED = "L"
        HIDDEN = "H"
        INTERNAL = "I"

    template = models.ForeignKey(AddonTemplate, on_delete=models.CASCADE, related_name="fields")
    key = models.SlugField(max_length=60)
    label_key = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=Type.choices)
    validation = models.JSONField(default=dict, blank=True)  # e.g. {"choices": [...], "max_length": 80}
    required_for_publish = models.BooleanField(default=False)
    show = models.CharField(max_length=1, choices=Show.choices, default=Show.PUBLIC)
    filterable = models.BooleanField(default=False)
    row_descriptor = models.BooleanField(default=False)
    provisional = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    deprecated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["template", "key"], name="uniq_addon_field")]


class ListTypeSettings(models.Model):
    concept = models.OneToOneField(Concept, on_delete=models.CASCADE, related_name="settings")
    index_threshold = models.PositiveIntegerField(default=10)
    row_descriptor_field = models.CharField(max_length=60, blank=True)
    actions_allowed = models.JSONField(default=list, blank=True)
    share_hidden = models.BooleanField(default=False)
    is_individual = models.BooleanField(default=False)
    is_child_facing = models.BooleanField(default=False)
    is_health = models.BooleanField(default=False)
    price_required_date = models.BooleanField(default=True)


class ReservedSlug(models.Model):
    """Place and list-type slugs share one URL namespace; this table keeps them from colliding (plan 8.2)."""
    slug = models.SlugField(max_length=120)
    kind = models.CharField(max_length=10)  # place | list_type | system

    class Meta:
        constraints = [models.UniqueConstraint(fields=["slug", "kind"], name="uniq_reserved_slug_kind")]
