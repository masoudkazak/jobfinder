from django.db import models

from apps.core.models import TimeStampedModel
from apps.jobs.models import Skill


class TelegramUser(TimeStampedModel):
    SLARY_TYPE_CHOICES = (
        ("fixed", "قیمت ثابت"),
        ("negotiable", "توافقی"),
    )

    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    skills = models.ManyToManyField(Skill, blank=True)
    province = models.JSONField(default=list, blank=True)
    remote_only = models.BooleanField(default=False)
    job_types = models.JSONField(default=list, blank=True)
    seniorities = models.JSONField(default=list, blank=True)
    salary = models.PositiveBigIntegerField(blank=True, null=True)
    salary_type = models.CharField(
        max_length=20, choices=SLARY_TYPE_CHOICES, default="fixed"
    )

    def __str__(self):
        return f"Telegram User {self.telegram_id}"
