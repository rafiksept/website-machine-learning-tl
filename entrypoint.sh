#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
python manage.py migrate

# Start Celery worker
celery -A trafficlight worker --loglevel=info &

# Start Celery beat
celery -A trafficlight beat --loglevel=info &

# Start Django server
exec "$@"
