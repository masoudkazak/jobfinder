import os

from decouple import config
from django.core.wsgi import get_wsgi_application

django_env = config("ENVIRONMENT", "dev")
if django_env == "dev":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")

application = get_wsgi_application()
