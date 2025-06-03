from rest_framework.serializers import ModelSerializer

from .models import TelegramUser


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = [
            "telegram_id",
            "username",
            "title",
            "skills",
            "province",
            "remote_only",
            "job_types",
            "seniorities",
            "salary_type",
            "min_salary",
            "max_salary",
        ]
