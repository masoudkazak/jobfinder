from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import JobPosting


class JobListSerializer(ModelSerializer):
    province = serializers.SerializerMethodField()

    class Meta:
        model = JobPosting
        fields = (
            "title",
            "company_persian",
            "company_english",
            "province",
            "is_remote",
            "description",
            "url",
            "job_type",
            "seniority_level",
            "salary",
            "salary_type",
            "source",
            "skills",
            "military_status",
            "source",
        )

    def get_province(self, obj):
        return obj.province.name
