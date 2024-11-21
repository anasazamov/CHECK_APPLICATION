from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django sozlamalarini avtomatik aniqlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Celery ilovasini yaratish
app = Celery("my_project")

# Django sozlamalarini Celeryga yuklash
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django ilovalaridagi vazifalarni avtomatik aniqlash
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
