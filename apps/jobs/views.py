from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from .filters import JobFilter
from .models import JobPosting
from .serializers import JobListSerializer


class JobListAPIView(ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter
