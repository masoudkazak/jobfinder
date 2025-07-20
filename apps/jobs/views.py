from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .filters import JobFilter
from .models import JobPosting
from .serializers import JobListSerializer


class JobListAPIView(ListAPIView):
    queryset = JobPosting.objects.all()
    serializer_class = JobListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def list(self, request, *args, **kwargs):
        telegram_id = request.query_params.get("telegram_id")

        if not telegram_id:
            return super().list(request, *args, **kwargs)

        cache_key = f"job_list_user:{telegram_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 60)
        return response
