import json

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
import django_filters

from .models import JobPosting


class JobFilter(django_filters.FilterSet):
    skills = django_filters.CharFilter(method="filter_skills")
    seniority_level = django_filters.CharFilter(method="filter_seniority")
    provinces = django_filters.CharFilter(method="filter_by_province_names")
    min_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="gte")
    max_salary = django_filters.NumberFilter(field_name="salary", lookup_expr="lte")
    title = django_filters.CharFilter(method="filter_title_similarity")
    description = django_filters.CharFilter(method="filter_description_similarity")
    job_type = django_filters.CharFilter(method="filter_job_type")

    class Meta:
        model = JobPosting
        fields = (
            "title",
            "is_remote",
            "description",
            "job_type",
            "seniority_level",
            "salary",
            "salary_type",
            "skills",
        )

    def parse_list(self, value):
        try:
            return json.loads(value)
        except Exception:
            return value.split(",")

    def filter_skills(self, queryset, name, value):
        skills = self.request.GET.getlist("skills") or self.parse_list(value)
        query = Q()
        for skill in skills:
            query |= Q(skills__icontains=skill)
        return queryset.filter(query)

    def filter_job_type(self, queryset, name, value):
        job_types = self.request.GET.getlist(name) or self.parse_list(value)
        return queryset.filter(job_type__in=job_types)

    def filter_seniority(self, queryset, name, value):
        levels = self.request.GET.getlist("seniority_level") or self.parse_list(value)
        query = Q()
        for level in levels:
            query |= Q(seniority_level__icontains=level)
        return queryset.filter(query)

    def filter_by_province_names(self, queryset, name, value):
        provinces = self.request.GET.getlist("provinces") or self.parse_list(value)
        return queryset.filter(province__name__in=provinces)

    def filter_title_similarity(self, queryset, name, value):
        return queryset.annotate(
            title_similarity=TrigramSimilarity("title", value)
        ).filter(title_similarity__gt=0.1)

    def filter_description_similarity(self, queryset, name, value):
        return queryset.filter(description__icontains=value)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        title_value = self.data.get("title")
        desc_value = self.data.get("description")

        queries = Q()

        if title_value:
            queryset = queryset.annotate(
                title_similarity=TrigramSimilarity("title", title_value)
            )
            queries |= Q(title_similarity__gt=0.05)

        if desc_value:
            queries |= Q(description__icontains=desc_value)

        if queries:
            queryset = queryset.filter(queries)

        if title_value:
            queryset = queryset.order_by("-title_similarity")

        return queryset
