#!/bin/bash

set -e

python manage.py wait_for_db
python manage.py migrate --noinput
python manage.py seed_provinces

cat ./ecommerce.asci || echo "ascii file not found."

if [ "$ENVIRONMENT" = "dev" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    $RELOAD \
    config.wsgi:application
fi
