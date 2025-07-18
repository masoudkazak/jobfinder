from rest_framework.generics import GenericAPIView, RetrieveAPIView

from .mixins import TelegramUserCreateUpdateRetrieveMixin
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramUserCreateUpdateRetrieveView(
    TelegramUserCreateUpdateRetrieveMixin,
    GenericAPIView,
):
    serializer_class = TelegramUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)


class MyTelegramProfile(RetrieveAPIView):
    serializer_class = TelegramUserSerializer
    queryset = TelegramUser.objects.all()
    lookup_field = "telegram_id"
