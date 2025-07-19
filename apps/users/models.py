from django.db import models

from apps.core.models import TimeStampedModel


class TelegramUser(TimeStampedModel):
    SLARY_TYPE_CHOICES = (
        ("fixed", "قیمت ثابت"),
        ("negotiable", "توافقی"),
    )

    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    province = models.JSONField(default=list, blank=True)
    remote_only = models.BooleanField(blank=True, null=True)
    job_types = models.JSONField(default=list, blank=True)
    seniorities = models.JSONField(default=list, blank=True)
    min_salary = models.PositiveBigIntegerField(blank=True, null=True)
    max_salary = models.PositiveBigIntegerField(blank=True, null=True)
    salary_type = models.CharField(
        max_length=20, choices=SLARY_TYPE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"Telegram User {self.telegram_id}"
