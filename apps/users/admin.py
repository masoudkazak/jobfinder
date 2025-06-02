from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "remote_only")
    list_filter = ("remote_only",)
    search_fields = (
        "telegram_id",
        "username",
    )
    filter_horizontal = ("skills",)
