from django.urls import path

from . import views

urlpatterns = [
    path(
        "create-update-telegram-user/",
        views.TelegramUserCreateUpdateRetrieveView.as_view(),
        name="create_update_telegram_user",
    ),
    path(
        "profile/<int:telegram_id>/",
        views.MyTelegramProfile.as_view(),
        name="my-telegram-profile",
    ),
]
