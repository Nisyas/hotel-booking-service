from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room",
        "date_start",
        "date_end",
        "duration_days",
        "total_price",
        "created_at",
    )
    list_filter = ("date_start", "created_at")
    search_fields = ("room__name",)
    ordering = ("date_start",)
    readonly_fields = ("created_at", "duration_days", "total_price")
    autocomplete_fields = ("room",)
