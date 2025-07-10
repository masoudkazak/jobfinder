from django.db import models

from apps.core.models import Province, TimeStampedModel


class JobPosting(TimeStampedModel):
    SLARY_TYPE_CHOICES = (
        ("fixed", "قیمت ثابت"),
        ("negotiable", "توافقی"),
    )
    title = models.CharField(max_length=255)
    company_persian = models.CharField(max_length=255)
    company_english = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    is_remote = models.BooleanField(default=False)

    description = models.TextField()
    url = models.URLField(max_length=2083, unique=True)

    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full_time", "تمام وقت"),
            ("part_time", "پاره‌ وقت"),
            ("contract", "قراردادی"),
            ("internship", "کارآموزی"),
        ],
    )

    seniority_level = models.JSONField(blank=True, null=True)

    salary = models.PositiveBigIntegerField(blank=True, null=True)
    salary_type = models.CharField(
        max_length=20, choices=SLARY_TYPE_CHOICES, default="fixed"
    )
    source = models.CharField(max_length=100)
    skills = models.JSONField(blank=True, null=True)

    military_status = models.JSONField(blank=True, null=True)
    source = models.CharField(max_length=50)

    class Meta:
        ordering = ("-created_at",)
        indexes = (
            models.Index(fields=["title"]),
            models.Index(fields=["province"]),
        )

    def __str__(self):
        return f"{self.title} at {self.company_english}"
