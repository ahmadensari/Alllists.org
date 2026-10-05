from django.contrib import admin

from . import models


class CheckInline(admin.TabularInline):
    model = models.Check
    extra = 0


class ContactInline(admin.TabularInline):
    model = models.Contact
    extra = 0


class SocialInline(admin.TabularInline):
    model = models.SocialLink
    extra = 0


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("name", "place", "plan", "status", "sponsored")
    list_filter = ("plan", "status", "sponsored", "list_types")
    search_fields = ("name", "name_alt")
    inlines = [CheckInline, ContactInline, SocialInline]


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "parent", "country_code")
    list_filter = ("kind",)
    search_fields = ("name",)


for m in (models.ListType, models.Profile, models.Enquiry, models.Report, models.Contribution,
          models.Sale, models.LedgerLine):
    admin.site.register(m)
