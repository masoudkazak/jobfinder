from rest_framework.generics import ListAPIView

from .models import JobPosting
from .serializers import JobListSerializer


class JobListAPIView(ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobListSerializer
