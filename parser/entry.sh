#!/bin/sh

if [ "$DATABASE" = "mariaDB" ]
then
    echo "Waiting for db..."

    while ! nc -z db 3306; do
      sleep 0.1
    done

    echo "MariaDB started"
fi

#python manage.py flush --no-input
python manage.py migrate

exec "$@"
