from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/users/", include("apps.users.urls")),
]
