from django.contrib import admin

from .models import CheckIn, Reflection


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "barrier", "suggestion_source", "ai_latency_ms", "created_at")
    list_filter = ("suggestion_source", "barrier")


admin.site.register(Reflection)
