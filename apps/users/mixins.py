from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .models import TelegramUser


class TelegramUserCreateUpdateRetrieveMixin(
    CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
):
    def create_or_update(self, request, *args, **kwargs):
        salary_type = request.data.get("salary", {})

        data = {
            "telegram_id": request.data.get("user_id"),
            "username": request.data.get("username"),
            "title": request.data.get("title", None),
            "skills": request.data.get("skills", []),
            "province": request.data.get("province", []),
            "remote_only": request.data.get("remote", False),
            "job_types": request.data.get("contract", []),
            "seniorities": request.data.get("level", []),
            "salary_type": salary_type.get("type", None),
            "min_salary": (
                salary_type.get("min", None)
                if salary_type.get("type", None) == "fixed"
                else None
            ),
            "max_salary": (
                salary_type.get("max", None)
                if salary_type.get("type", None) == "fixed"
                else None
            ),
        }
        telegram_user_id = request.data.get("user_id", None)
        telegram_user = TelegramUser.objects.filter(
            telegram_id=telegram_user_id
        ).first()
        if telegram_user:
            serializer = self.serializer_class(telegram_user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
