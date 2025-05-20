import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        auto_created=True, primary_key=True, default=uuid.uuid4, editable=False
    )

    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        indexes = (
            models.Index(fields=["username"], name="users_user_username_ind"),
            models.Index(fields=["email"], name="users_user_email_ind"),
        )
