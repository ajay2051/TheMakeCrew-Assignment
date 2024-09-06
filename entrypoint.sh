#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
echo "================================ Sever is starting now  =================================="
python3 manage.py migrate &

#gunicorn --bind 0.0.0.0:8000 --reload project.wsgi
python3 manage.py runserver 0.0.0.0:8000
