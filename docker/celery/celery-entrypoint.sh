#!/bin/bash
set -e

until nc -z rabbitmq 5672; do
  echo "🕒 Waiting for RabbitMQ..."
  sleep 1
done

if [ "$CELERY_WORKER_TYPE" = "beat" ]; then
    echo "Starting Celery Beat..."
    celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
else
    echo "Starting Celery Worker..."
    celery -A config worker -l info
fi
