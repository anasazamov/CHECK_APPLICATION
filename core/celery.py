from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings modulini ko‘rsatish
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Celery ilovasini yaratish
app = Celery('core')

# Django settings-dan konfiguratsiyalarni yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Berilgan vazifalarni avtomatik kashf qilish
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
