import os

from dotenv import load_dotenv
from settings.base import *  # noqa: F403

load_dotenv()


ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
DEBUG = os.getenv("DEBUG") == "True"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
STATIC_URL = os.getenv("STATIC_URL")
STATIC_ROOT = os.getenv("STATIC_ROOT")
MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = os.getenv("MEDIA_ROOT")
