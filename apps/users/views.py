from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsOwnerUser
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserRetrieveSerializer,
)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerUser)
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class LoginAPIView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
