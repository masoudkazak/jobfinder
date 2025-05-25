import os

from decouple import config

from celery import Celery

django_env = config("ENVIRONMENT", "dev")
if django_env == "dev":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

celery_app = Celery("config")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
