from django.contrib import admin

from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company_english",
        "province",
        "is_remote",
        "source",
        "created_at",
    )
    search_fields = ("title", "skills", "description")
    list_filter = (
        "source",
        "is_remote",
        "job_type",
    )
