from django.db import models


class CICharField(models.CharField):
    def db_type(self, connection):
        return "citext"
