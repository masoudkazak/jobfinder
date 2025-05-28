from rest_framework.serializers import ModelSerializer

from .models import JobPosting


class JobListSerializer(ModelSerializer):
    class Meta:
        model = JobPosting
        fields = "__all__"
