#!/bin/bash


python manage.py wait_for_db
python manage.py migrate --noinput


cat /karsaz/ecommerce.asci

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application
