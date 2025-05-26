from django.db import models

from apps.core.models import TimeStampedModel
from apps.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    BUDGET_TYPE_CHOICES = (
        ("fixed", "قیمت ثابت"),
        ("negotiable", "توافقی"),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget_type = models.CharField(
        max_length=20, choices=BUDGET_TYPE_CHOICES, default="fixed"
    )
    budget_min = models.PositiveBigIntegerField(null=True, blank=True)
    budget_max = models.PositiveBigIntegerField(null=True, blank=True)
    deadline = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    required_skills = models.ManyToManyField(Skill)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title
