from decouple import config

from .base import *  # noqa: F403

ALLOWED_HOSTS = config("ALLOWED_HOSTS", "").split(",")
DEBUG = config("DEBUG") == "True"
SECRET_KEY = config("DJANGO_SECRET_KEY")
STATIC_URL = config("STATIC_URL")
