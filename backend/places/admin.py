from django.contrib import admin

from .models import Place, PlaceName, PlaceProposal


class PlaceNameInline(admin.TabularInline):
    model = PlaceName
    extra = 0


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("path", "level", "country_code", "status")
    list_filter = ("level", "status", "country_code")
    search_fields = ("path", "slug")
    inlines = [PlaceNameInline]


admin.site.register(PlaceProposal)
