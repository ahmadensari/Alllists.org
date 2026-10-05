"""Data model. Places form a tree; list types are categories; a *list* is a view (list type at a place).
Entries are stored once and roll up the tree. Contacts are stored but never rendered to visitors."""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.text import slugify


class Place(models.Model):
    class Kind(models.TextChoices):
        WORLD = "world"
        COUNTRY = "country"
        REGION = "region"
        CITY = "city"
        AREA = "area"

    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    name = models.CharField(max_length=120)
    name_ur = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(max_length=140)
    country_code = models.CharField(max_length=2, blank=True)  # partition key

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["parent", "slug"], name="uniq_place_slug_per_parent")]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def label(self, lang):
        return (self.name_ur if lang == "ur" and self.name_ur else self.name)

    def ancestors(self):
        chain, node = [], self
        while node:
            chain.append(node)
            node = node.parent
        return list(reversed(chain))

    def descendant_ids(self):
        ids, frontier = [self.pk], [self.pk]
        while frontier:
            frontier = list(Place.objects.filter(parent_id__in=frontier).values_list("pk", flat=True))
            ids += frontier
        return ids

    @property
    def path(self):
        return "/".join(p.slug for p in self.ancestors()[1:])


class ListType(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    name_ur = models.CharField(max_length=120, blank=True)
    group = models.CharField(max_length=60, blank=True)
    # add-on field registry: which extra fields this type uses (decision: one registry per list type)
    addon_fields = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def label(self, lang):
        return self.name_ur if lang == "ur" and self.name_ur else self.name


class Entry(models.Model):
    class Plan(models.TextChoices):
        BASIC = "basic"
        COMPANY = "company"   # paid company page: same template, more sections

    class Status(models.TextChoices):
        ACTIVE = "active"
        CLOSED = "closed"
        MOVED = "moved"

    name = models.CharField(max_length=200)
    name_alt = models.CharField(max_length=200, blank=True)
    place = models.ForeignKey(Place, on_delete=models.PROTECT, related_name="entries")  # most specific place
    list_types = models.ManyToManyField(ListType, related_name="entries")
    entry_type = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    website = models.URLField(blank=True)
    size = models.CharField(max_length=60, blank=True)
    markets = models.CharField(max_length=200, blank=True)
    moq = models.CharField(max_length=80, blank=True)
    price_note = models.CharField(max_length=200, blank=True)
    certificates = models.CharField(max_length=300, blank=True)
    specialities = models.JSONField(default=list, blank=True)
    extra = models.JSONField(default=dict, blank=True)  # add-on block values
    plan = models.CharField(max_length=10, choices=Plan.choices, default=Plan.BASIC)
    company_profile = models.TextField(blank=True)  # provided by the company, shown only on company pages
    sponsored = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sponsored", "name"]
        verbose_name_plural = "entries"
        indexes = [models.Index(fields=["place", "status"])]

    def __str__(self):
        return self.name

    @property
    def is_company(self):
        return self.plan == self.Plan.COMPANY

    def last_checked(self):
        c = self.checks.order_by("-checked_on").first()
        return c.checked_on if c else None

    def best_level(self):
        order = [Check.Level.SURVEYOR, Check.Level.OWNER, Check.Level.AI]
        have = {c.level for c in self.checks.all()}
        for lv in order:
            if lv in have:
                return lv
        return Check.Level.NONE


class Check(models.Model):
    """Per-field provenance: who verified what, and when. Four decided labels."""
    class Level(models.TextChoices):
        SURVEYOR = "surveyor"
        OWNER = "owner"
        AI = "ai"
        NONE = "none"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="checks")
    field = models.CharField(max_length=40, default="entry")
    level = models.CharField(max_length=10, choices=Level.choices)
    checked_on = models.DateField()
    checked_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-checked_on"]


class Contact(models.Model):
    """Phone, WhatsApp, email. Stored for the outreach relay only; never shown on a page."""
    class Kind(models.TextChoices):
        PHONE = "phone"
        WHATSAPP = "whatsapp"
        EMAIL = "email"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="contacts")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    value = models.CharField(max_length=200)


class SocialLink(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="socials")
    channel = models.CharField(max_length=30)
    url = models.URLField()


class Service(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="services")
    text = models.CharField(max_length=200)


class Identifier(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="identifiers")
    scheme = models.CharField(max_length=40)
    value = models.CharField(max_length=80)


class Profile(models.Model):
    """Viewer plan (Free or Subscriber). Distinct from an entry's listing plan."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscriber = models.BooleanField(default=False)
    contributor = models.BooleanField(default=False)


class Enquiry(models.Model):
    """One message relayed to many suppliers. Supplier contacts are used by the relay, never revealed."""
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    entries = models.ManyToManyField(Entry, related_name="enquiries")
    reply_to = models.EmailField()
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    relayed_at = models.DateTimeField(null=True, blank=True)


class Report(models.Model):
    class Kind(models.TextChoices):
        REPORT = "report"
        CLAIM = "claim"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="reports")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    note = models.TextField(max_length=1000, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


class Contribution(models.Model):
    """A contributor's entry. The share rate is locked when the entry is accepted (phase 1/2/3 = 50/40/30)."""
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="contribution")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phase = models.PositiveSmallIntegerField()
    rate_percent = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def lock(cls, entry, user):
        phase = settings.CURRENT_PHASE
        return cls.objects.create(entry=entry, user=user, phase=phase,
                                  rate_percent=settings.CONTRIBUTOR_PHASE_RATES[phase])


class Sale(models.Model):
    """A list (list type at a place) sold. Revenue is shared only when a list sells."""
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    list_type = models.ForeignKey(ListType, on_delete=models.PROTECT)
    amount_cents = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    distributed = models.BooleanField(default=False)

    def distribute(self):
        """Split the sale equally across the list's entries; each contributor gets that slice at the
        rate locked for their entry. Idempotent; returns the ledger lines created."""
        if self.distributed:
            return []
        entries = list(Entry.objects.filter(
            Q(place_id__in=self.place.descendant_ids()), list_types=self.list_type, status=Entry.Status.ACTIVE))
        lines = []
        if entries:
            slice_cents = self.amount_cents // len(entries)
            for e in entries:
                c = getattr(e, "contribution", None)
                if c:
                    lines.append(LedgerLine.objects.create(
                        sale=self, entry=e, user=c.user, rate_percent=c.rate_percent,
                        amount_cents=slice_cents * c.rate_percent // 100))
        self.distributed = True
        self.save(update_fields=["distributed"])
        return lines


class LedgerLine(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="lines")
    entry = models.ForeignKey(Entry, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rate_percent = models.PositiveSmallIntegerField()
    amount_cents = models.PositiveBigIntegerField()
