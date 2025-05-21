from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("<uuid:pk>/", views.UserRetrieveUpdateAPIView.as_view(), name="register"),
    path("register/", views.UserCreateAPIView.as_view(), name="register"),
]
