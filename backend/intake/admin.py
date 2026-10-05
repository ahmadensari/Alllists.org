from django.contrib import admin

from .models import DedupeCandidate, ImportBatch, ImportRow, Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "tier", "status", "reviewed_on", "bulk_permission")
    list_filter = ("tier", "status")


admin.site.register([ImportBatch, ImportRow, DedupeCandidate])
