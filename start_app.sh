#!/bin/bash

echo "Начало установки..."

until python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('db', 5432)); s.close()" 2>/dev/null; do
    sleep 3
done

echo "База данных запустилась"

python manage.py collectstatic && echo "collectstatic выполнена"

python manage.py migrate && echo "migrate выполнена"

DJANGO_SUPERUSER_PASSWORD="$admin_password" python manage.py createsuperuser --noinput \
  --username "$admin_user" --email "" 2>/dev/null \
  || echo "суперпользователь уже существует"

python manage.py create_roles

exec python manage.py runserver 0.0.0.0:8000