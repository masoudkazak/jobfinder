from django.db import models

from apps.core.models import Province, TimeStampedModel


class JobPosting(TimeStampedModel):
    SLARY_TYPE_CHOICES = (
        ("fixed", "قیمت ثابت"),
        ("negotiable", "توافقی"),
    )
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    is_remote = models.BooleanField(default=False)

    description = models.TextField()
    url = models.URLField(max_length=1000)

    job_type = models.CharField(
        max_length=50,
        choices=[
            ("full_time", "تمام‌وقت"),
            ("part_time", "پاره‌وقت"),
            ("contract", "قراردادی"),
            ("internship", "کارآموزی"),
        ],
    )

    seniority_level = models.CharField(
        max_length=50,
        choices=[
            ("junior", "Junior"),
            ("mid", "Mid"),
            ("senior", "Senior"),
            ("lead", "Lead"),
        ],
    )

    salary = models.PositiveBigIntegerField(blank=True, null=True)
    salary_type = models.CharField(
        max_length=20, choices=SLARY_TYPE_CHOICES, default="fixed"
    )
    source = models.CharField(max_length=100)
    posted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    skills = models.JSONField(blank=True, null=True)

    military_status = models.CharField(max_length=50, blank=True, null=True)
    job_url = models.URLField(unique=True)
    source = models.CharField(max_length=50)

    class Meta:
        ordering = ("-posted_at",)
        indexes = (
            models.Index(fields=["title"]),
            models.Index(fields=["company"]),
            models.Index(fields=["province"]),
        )

    def __str__(self):
        return f"{self.title} at {self.company}"
