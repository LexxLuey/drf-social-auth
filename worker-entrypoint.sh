#!/bin/sh

until cd /app/core
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A core worker -l info -B
