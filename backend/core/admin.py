from django.contrib import admin

from .models import AuditLog, ChangeLog, CountrySwitch, FeatureFlag, RegistryVersion


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "ts", "action", "object_type", "object_uid", "actor_id")
    search_fields = ("action", "object_uid")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CountrySwitch)
class CountrySwitchAdmin(admin.ModelAdmin):
    list_display = ("country_code", "browsing_on", "indexing_on", "selling_on", "outreach_on", "ads_on", "cleared_by")


admin.site.register([ChangeLog, FeatureFlag, RegistryVersion])
