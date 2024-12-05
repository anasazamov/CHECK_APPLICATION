#!/bin/sh


echo "Starting Redis server..."
redis-server --daemonize yes

echo "Applying Django migrations..."
python manage.py migrate

echo "Creating Django superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from check_server.models import Company
User = get_user_model()
user = User.objects.filter(username="admin")
if not user.exists():
    user = User.objects.create_superuser("admin", "admin@example.com", "admin")
else:
    user = user.first()
company = Company.objects.filter(name="Cradle Vision", user=user)
if not company.exists():
    company = Company.objects.create(name="Cradle Vision")
    company.user.add(user)
EOF

echo "Starting Celery worker..."
celery -A core worker --loglevel=info &

echo "Starting Celery beat..."
celery -A core beat --loglevel=info &

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000 &

wait
