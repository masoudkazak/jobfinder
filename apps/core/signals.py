# apps/users/signals.py
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import psycopg2


@receiver(connection_created)
def activate_citext_extension(sender, connection, **kwargs):
    if connection.vendor == "postgresql":
        with connection.cursor() as cursor:
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS citext;")
            except psycopg2.ProgrammingError:
                pass
