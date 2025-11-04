import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'highload_3hw.settings')
app = Celery('highload_3hw')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()