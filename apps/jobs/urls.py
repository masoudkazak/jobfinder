from django.urls import path

from . import views

urlpatterns = [
    path("", views.JobListAPIView.as_view(), name="list-jobs"),
]
