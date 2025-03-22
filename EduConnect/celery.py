# EduConnect/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduConnect.settings')

# Create a Celery application instance with the project name
app = Celery('EduConnect')

# Use a string here to avoid having to serialize the configuration object to child processes.
# 'namespace'='CELERY' ensures all Celery-related configuration keys have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover task modules from all registered Django app configs.
app.autodiscover_tasks()

# Define the periodic task schedule using Celery Beat
app.conf.beat_schedule = {
    'delete-expired-rooms-every-minute': {
        'task': 'chat.tasks.delete_expired_rooms',
        'schedule': crontab(minute='*/1'),  # Schedule to run every minute
    },
}

# Configure logging to use Django's logging settings
@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig
    dictConfig(settings.LOGGING)
