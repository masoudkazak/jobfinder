import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from apps.core.fields import CICharField


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(
        auto_created=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    username = CICharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = CICharField(unique=True)
    is_client = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)

    class Meta:
        indexes = (
            models.Index(fields=["username"], name="users_user_username_ind"),
            models.Index(fields=["email"], name="users_user_email_ind"),
        )

    def __str__(self):
        return self.email
