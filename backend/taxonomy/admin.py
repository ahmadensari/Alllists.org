from django.contrib import admin

from .models import AddonField, AddonTemplate, Concept, ConceptCrosswalk, ConceptLabel, ListTypeSettings, ReservedSlug


class LabelInline(admin.TabularInline):
    model = ConceptLabel
    extra = 0


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("slug", "kind", "natural_scale", "status")
    list_filter = ("kind", "natural_scale")
    search_fields = ("slug", "labels__text")
    inlines = [LabelInline]


class AddonFieldInline(admin.TabularInline):
    model = AddonField
    extra = 0


@admin.register(AddonTemplate)
class AddonTemplateAdmin(admin.ModelAdmin):
    list_display = ("key", "version", "status")
    inlines = [AddonFieldInline]


admin.site.register([ConceptCrosswalk, ListTypeSettings, ReservedSlug])
