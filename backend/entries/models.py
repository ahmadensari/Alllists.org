"""Entries, child records, per-field provenance and verification (plan sections 4.2.4, 6)."""

from django.conf import settings
from django.db import models

from core import clock
from core.crypto import EncryptedTextField
from core.models import SoftDeleteModel, UidModel


class Entry(UidModel, SoftDeleteModel):
    class EntityType(models.TextChoices):
        BUSINESS = "business"
        FACILITY = "facility"
        PERSON = "person"
        INSTITUTION = "institution"

    class Status(models.TextChoices):
        OPEN = "open"
        TEMP_CLOSED = "temporarily_closed"
        PERM_CLOSED = "permanently_closed"
        MOVED = "moved"

    class PublishState(models.TextChoices):
        DRAFT = "draft"
        REVIEW = "review"
        PUBLISHED = "published"
        SUPPRESSED = "suppressed"
        TOMBSTONED = "tombstoned"

    class ClaimState(models.TextChoices):
        UNCLAIMED = "unclaimed"
        PENDING = "pending"
        CLAIMED = "claimed"

    class CreatedVia(models.TextChoices):
        CONTRIBUTOR = "contributor"
        IMPORT = "import"
        AGENT = "agent"
        REGISTER = "register"
        SELF = "self"

    country_code = models.CharField(max_length=2, db_index=True)
    entity_type = models.CharField(max_length=12, choices=EntityType.choices, default=EntityType.BUSINESS)
    primary_concept = models.ForeignKey("taxonomy.Concept", on_delete=models.PROTECT, related_name="+")
    secondary_concepts = models.ManyToManyField("taxonomy.Concept", blank=True, related_name="secondary_entries")
    name = models.CharField(max_length=250)
    name_lang = models.CharField(max_length=10, default="en")
    name_fold = models.CharField(max_length=250, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    status_date = models.DateField(null=True, blank=True)
    publish_state = models.CharField(max_length=12, choices=PublishState.choices, default=PublishState.DRAFT)
    address = models.JSONField(default=dict, blank=True)
    address_text = models.CharField(max_length=400, blank=True)
    place = models.ForeignKey("places.Place", on_delete=models.PROTECT, related_name="entries")
    place_path = models.CharField(max_length=500)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    precision_class = models.CharField(max_length=10, blank=True)
    coord_source = models.CharField(max_length=40, blank=True)
    coord_date = models.DateField(null=True, blank=True)
    service_area = models.JSONField(default=dict, blank=True)
    website = models.URLField(blank=True)
    size_band = models.CharField(max_length=20, blank=True)
    year_established = models.PositiveSmallIntegerField(null=True, blank=True)
    parent_entry = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="branches_of"
    )
    languages = models.JSONField(default=list, blank=True)
    price_band = models.CharField(max_length=10, blank=True)
    payment_methods = models.JSONField(default=list, blank=True)
    addons = models.JSONField(default=dict, blank=True)
    addon_template_version = models.PositiveIntegerField(null=True, blank=True)
    claim_state = models.CharField(max_length=10, choices=ClaimState.choices, default=ClaimState.UNCLAIMED)
    listing_plan = models.CharField(max_length=10, default="basic")
    plan_valid_until = models.DateField(null=True, blank=True)
    visibility_flags = models.JSONField(default=list, blank=True)  # do_not_share, noindex, suppressed
    created_via = models.CharField(max_length=12, choices=CreatedVia.choices, default=CreatedVia.CONTRIBUTOR)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    source = models.ForeignKey("intake.Source", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    phase_id = models.PositiveIntegerField(
        null=True, blank=True
    )  # locked rate phase (rule R11), set by the ledger module
    created_at = models.DateTimeField(default=clock.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_verified_at = models.DateTimeField(null=True, blank=True)
    merged_into = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="merged_from"
    )

    class Meta:
        verbose_name_plural = "entries"
        indexes = [
            models.Index(
                fields=["country_code", "place_path", "primary_concept", "publish_state"], name="entry_list_query"
            ),
            models.Index(fields=["country_code", "claim_state"], name="entry_claim_idx"),
        ]

    def __str__(self):
        return self.name


# ---- child records (plan 4.2.4) ----------------------------------------------------------------------------


class EntryChild(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="%(class)s_set")
    country_code = models.CharField(max_length=2)

    class Meta:
        abstract = True


class NameVariant(EntryChild):
    text = models.CharField(max_length=250)
    language = models.CharField(max_length=10, blank=True)
    kind = models.CharField(max_length=15, default="trade")  # legal, trade, old, transliteration
    text_fold = models.CharField(max_length=250, db_index=True)


class Contact(EntryChild):
    """Never rendered to anyone (rule R02). Value is encrypted; the keyed hash allows lookups and suppression."""

    class Kind(models.TextChoices):
        PHONE = "phone"
        MOBILE = "mobile"
        WHATSAPP = "whatsapp"
        EMAIL = "email"
        FAX = "fax"

    kind = models.CharField(max_length=10, choices=Kind.choices)
    value_enc = EncryptedTextField()
    value_hash = models.CharField(max_length=64, db_index=True)
    label = models.CharField(max_length=20, blank=True)
    preferred_hours = models.CharField(max_length=60, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    relay_only = models.BooleanField(default=True, editable=False)
    optin_state = models.CharField(max_length=12, default="none")


class Social(EntryChild):
    platform = models.CharField(max_length=30)
    handle_or_url = models.CharField(max_length=300)
    owner_confirmed = models.BooleanField(default=False)
    last_link_check = models.DateTimeField(null=True, blank=True)
    link_status = models.CharField(max_length=10, blank=True)


class Hours(EntryChild):
    day_from = models.PositiveSmallIntegerField()
    day_to = models.PositiveSmallIntegerField()
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    appointment_only = models.BooleanField(default=False)
    confirmed_on = models.DateField(null=True, blank=True)
    tz = models.CharField(max_length=40, blank=True)


class Service(EntryChild):
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    name_text = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_minor = models.BigIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True)
    price_type = models.CharField(max_length=10, blank=True)  # fixed, from, hourly, per_visit
    unit = models.CharField(max_length=40, blank=True)
    price_date = models.DateField(null=True, blank=True)
    prep_notes = models.CharField(max_length=300, blank=True)


class Product(EntryChild):
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    name_text = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=40, blank=True)
    price_band = models.CharField(max_length=10, blank=True)
    availability_note = models.CharField(max_length=200, blank=True)
    price_date = models.DateField(null=True, blank=True)


class Speciality(EntryChild):
    concept = models.ForeignKey("taxonomy.Concept", on_delete=models.PROTECT, related_name="+")
    qualification = models.CharField(max_length=200, blank=True)
    own_hours = models.CharField(max_length=120, blank=True)


class Identifier(EntryChild):
    """Store the fact and the register link, never a national ID number such as CNIC."""

    scheme = models.CharField(max_length=30)
    value = models.CharField(max_length=80)
    issuer = models.CharField(max_length=120, blank=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_to = models.DateField(null=True, blank=True)
    last_checked = models.DateField(null=True, blank=True)
    register_url = models.URLField(blank=True)


class AreaServed(EntryChild):
    place = models.ForeignKey("places.Place", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    radius_km = models.PositiveIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True)


class Equipment(EntryChild):
    type = models.CharField(max_length=80)
    make_model = models.CharField(max_length=120, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    modality = models.CharField(max_length=60, blank=True)
    installed_year = models.PositiveSmallIntegerField(null=True, blank=True)
    services_supported = models.JSONField(default=list, blank=True)


class Branch(EntryChild):
    address_text = models.CharField(max_length=400, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


# ---- provenance and verification (plan 6) ------------------------------------------------------------------


class ValueMeta(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="value_meta")
    country_code = models.CharField(max_length=2)
    field_key = models.CharField(max_length=60)
    source = models.ForeignKey("intake.Source", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    licence_text = models.CharField(max_length=200, blank=True)
    retrieved_at = models.DateTimeField(default=clock.now)
    level = models.CharField(max_length=10, default="none")
    verified_by_id = models.BigIntegerField(null=True, blank=True)
    method = models.CharField(max_length=40, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    evidence_text = models.TextField(blank=True)
    consent_ref = models.CharField(max_length=40, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = [("entry", "field_key")]


class VerificationEvent(models.Model):
    """Append-only (database trigger forbids update and delete)."""

    class Level(models.TextChoices):
        SURVEYOR = "surveyor"
        OWNER = "owner"
        AI = "ai"

    class State(models.TextChoices):
        PENDING = "pending"
        VERIFIED = "verified"
        EXPIRED = "expired"
        REVOKED = "revoked"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="verification_events")
    country_code = models.CharField(max_length=2)
    field_group = models.CharField(max_length=20)  # identity, location, contact, hours, services, certificates
    level = models.CharField(max_length=10, choices=Level.choices)
    state = models.CharField(max_length=10, choices=State.choices)
    actor_id = models.BigIntegerField(null=True, blank=True)
    method = models.CharField(max_length=40, blank=True)
    evidence_text = models.TextField(blank=True)
    source = models.ForeignKey("intake.Source", null=True, blank=True, on_delete=models.PROTECT, related_name="+")
    ts = models.DateTimeField(default=clock.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    supersedes = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name="+")

    class Meta:
        ordering = ["id"]


class VerificationCurrent(models.Model):
    """Projection the pages read. Rebuilt from events."""

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="verification_current")
    field_group = models.CharField(max_length=20)
    level = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    verified_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=40, blank=True)
    actor_display = models.CharField(max_length=80, blank=True)  # kept for old rows; never shown publicly
    actor_id = models.BigIntegerField(
        null=True, blank=True
    )  # who checked; a name is shown only if they chose to be credited

    class Meta:
        unique_together = [("entry", "field_group", "level")]


class Claim(models.Model):
    class State(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="claims")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+")
    method = models.CharField(max_length=20)  # otp_phone, otp_email, documents
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    evidence_text = models.TextField(blank=True)
    created_at = models.DateTimeField(default=clock.now)
    decided_by_id = models.BigIntegerField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)


class ConsentRecord(models.Model):
    """Append-only consent for individuals and contacts (rule R18)."""

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="consents")
    subject_kind = models.CharField(max_length=10, default="entry")  # entry | contact
    status = models.CharField(max_length=12)  # consented, withdrawn, takedown
    method = models.CharField(max_length=40)
    wording_version = models.CharField(max_length=20)
    evidence_text = models.TextField(blank=True)
    at = models.DateTimeField(default=clock.now)

    class Meta:
        ordering = ["id"]


class CreditEvent(models.Model):
    """Credit lives here, not on the entry, so duplicates can merge without losing first-adder credit (D6)."""

    entry = models.ForeignKey(Entry, null=True, on_delete=models.SET_NULL, related_name="credit_events")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    kind = models.CharField(max_length=20)  # added, verified, area_added, claimed_assist
    eligible = models.BooleanField(default=False)
    ineligible_reason = models.CharField(max_length=60, blank=True)
    phase_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=clock.now)
    merged_from_id = models.BigIntegerField(null=True, blank=True)


class MergeMap(models.Model):
    """Append-only record of a merge (plan 6.7). The dropped entry redirects to the kept one."""

    from_entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="+")
    to_entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="+")
    score = models.FloatField(null=True, blank=True)
    decided_by_id = models.BigIntegerField(null=True, blank=True)
    decided_at = models.DateTimeField(default=clock.now)


class CompanySection(models.Model):
    """Company-provided content for a paid company page (plan 8.3.3, rule R15). Public and labelled
    "Provided by the company"; moderated before it shows."""

    class Kind(models.TextChoices):
        ABOUT = "about"
        PRODUCTS = "products"
        CAPACITY = "capacity"
        TERMS = "terms"
        FAQ = "faq"

    class State(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="company_sections")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    title = models.CharField(max_length=160, blank=True)  # the question for FAQ rows
    body = models.TextField(max_length=4000)
    sort = models.PositiveSmallIntegerField(default=0)
    state = models.CharField(max_length=10, choices=State.choices, default=State.PENDING)
    updated_at = models.DateTimeField(default=clock.now)
    moderated_by_id = models.BigIntegerField(null=True, blank=True)


class StewardGrant(models.Model):
    """A revocable right to review and correct one place segment, optionally for one list type (plan 6.6, C20)."""

    class State(models.TextChoices):
        ACTIVE = "active"
        EXPIRED = "expired"
        REVOKED = "revoked"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="steward_grants")
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE, related_name="+")
    concept = models.ForeignKey("taxonomy.Concept", null=True, blank=True, on_delete=models.CASCADE, related_name="+")
    state = models.CharField(max_length=10, choices=State.choices, default=State.ACTIVE)
    granted_at = models.DateTimeField(default=clock.now)
    last_active_at = models.DateTimeField(default=clock.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    dispute_state = models.CharField(max_length=12, blank=True)
