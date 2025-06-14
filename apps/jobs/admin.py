from django.contrib import admin

from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "province", "is_remote", "source", "posted_at")
    search_fields = ("title", "company", "description")
    list_filter = ("source", "is_remote", "job_type", "seniority_level")
