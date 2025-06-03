from rest_framework.generics import GenericAPIView

from .mixins import TelegramUserCreateUpdateRetrieveMixin
from .serializers import TelegramUserSerializer


class TelegramUserCreateUpdateRetrieveView(
    TelegramUserCreateUpdateRetrieveMixin,
    GenericAPIView,
):
    serializer_class = TelegramUserSerializer

    def post(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)
