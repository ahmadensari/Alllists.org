"""Place tree (plan sections 4.2.2, 5.1). `path` makes "everything under Rawalpindi" one prefix range scan."""

from django.db import models
from django.db.models import Q

from core import clock
from core.models import UidModel


class Place(UidModel):
    class Level(models.TextChoices):
        WORLD = "world"
        REGION = "region"
        COUNTRY = "country"
        ADMIN1 = "admin1"
        ADMIN2 = "admin2"
        ADMIN3 = "admin3"
        CITY = "city"
        AREA = "area"
        SOCIETY = "society"
        STREET = "street"

    class Status(models.TextChoices):
        ACTIVE = "active"
        PROPOSED = "proposed"
        REJECTED = "rejected"
        MERGED = "merged"

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="children")
    level = models.CharField(max_length=10, choices=Level.choices)
    local_level_label = models.CharField(max_length=40, blank=True)
    iso_code = models.CharField(max_length=10, blank=True)
    country_code = models.CharField(max_length=2, blank=True, db_index=True)
    slug = models.SlugField(max_length=120)
    path = models.CharField(max_length=500, db_index=True)  # e.g. pk.punjab.rawalpindi.adyala; "" for the world
    depth = models.PositiveSmallIntegerField(default=0)
    centre_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    centre_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    population_band = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    source_id = models.BigIntegerField(null=True, blank=True)
    geonames_id = models.BigIntegerField(null=True, blank=True)
    wikidata_id = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=clock.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "slug"], name="places_uniq_slug_per_parent"),
            models.UniqueConstraint(fields=["slug"], condition=Q(parent__isnull=True), name="uniq_root_slug"),
        ]
        indexes = [models.Index(fields=["path"], name="place_path_prefix", opclasses=["varchar_pattern_ops"])]

    def __str__(self):
        return self.name_for("en")

    def name_for(self, language):
        names = list(self.names.all())
        for n in names:
            if n.language == language and n.kind == PlaceName.Kind.PREFERRED:
                return n.name
        for n in names:
            if n.kind == PlaceName.Kind.PREFERRED:
                return n.name
        return self.slug

    def ancestors(self):
        chain, node = [], self
        while node:
            chain.append(node)
            node = node.parent
        return list(reversed(chain))


class PlaceName(models.Model):
    class Kind(models.TextChoices):
        PREFERRED = "preferred"
        ALIAS = "alias"
        TRANSLITERATION = "transliteration"

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="names")
    language = models.CharField(max_length=10)  # BCP 47
    script = models.CharField(max_length=10, blank=True)
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.PREFERRED)
    name_fold = models.CharField(max_length=200, db_index=True)


class PlaceProposal(models.Model):
    """A user-added area (Adyala Road, Abraham Street) waits here for approval (Q-O2 default)."""

    class State(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"
        DUPLICATE = "duplicate"

    parent = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="proposals")
    proposed_name = models.CharField(max_length=200)
    language = models.CharField(max_length=10, default="en")
    proposer_id = models.BigIntegerField(null=True, blank=True)
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    duplicate_of = models.ForeignKey(Place, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    decided_by = models.BigIntegerField(null=True, blank=True)
    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=clock.now)


class PlaceExternalId(models.Model):
    """A place's id in an open dataset (Overture, GeoNames, Wikidata), so a repeat load updates instead of duplicating."""

    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="external_ids")
    scheme = models.CharField(max_length=20)
    value = models.CharField(max_length=80)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["scheme", "value"], name="uniq_place_external_id")]
