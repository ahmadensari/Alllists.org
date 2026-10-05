from django.contrib import admin

from .models import (
    Claim,
    ConsentRecord,
    Contact,
    CreditEvent,
    Entry,
    Identifier,
    NameVariant,
    Service,
    Social,
    VerificationCurrent,
)


class NameVariantInline(admin.TabularInline):
    model = NameVariant
    extra = 0


class SocialInline(admin.TabularInline):
    model = Social
    extra = 0


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


class IdentifierInline(admin.TabularInline):
    model = Identifier
    extra = 0


class CurrentInline(admin.TabularInline):
    model = VerificationCurrent
    extra = 0
    can_delete = False
    readonly_fields = ("field_group", "level", "state", "verified_at", "expires_at", "method", "actor_display")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Raw edits go through the service layer in the staff console (phase P2); admin is for staff inspection and seeding.
    Contact values are deliberately not shown here: they are encrypted and relay-only (rule R02)."""

    list_display = ("name", "country_code", "place_path", "publish_state", "claim_state", "created_via")
    list_filter = ("country_code", "publish_state", "claim_state", "created_via", "entity_type")
    search_fields = ("name", "name_fold", "uid")
    readonly_fields = ("uid", "name_fold", "place_path", "created_at", "updated_at", "last_verified_at")
    inlines = [NameVariantInline, SocialInline, ServiceInline, IdentifierInline, CurrentInline]


admin.site.register([Claim, ConsentRecord, CreditEvent])
admin.site.register(
    Contact,
    type(
        "ContactAdmin",
        (admin.ModelAdmin,),
        {"list_display": ("entry", "kind", "label", "optin_state"), "exclude": ("value_enc", "value_hash")},
    ),
)
