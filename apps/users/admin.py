from django.contrib import admin

from .models import UserFilterPreference


@admin.register(UserFilterPreference)
class UserFilterAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "remote_only")
    list_filter = ("remote_only",)
    search_fields = ("telegram_id", "username", "first_name", "last_name")
    filter_horizontal = ("skills",)
