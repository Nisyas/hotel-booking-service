from django.contrib import admin

from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
