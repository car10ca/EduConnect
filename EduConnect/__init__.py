from __future__ import absolute_import, unicode_literals  # Ensure compatibility with both Python 2 and 3
from .celery import app as celery_app  # Import the Celery application instance

__all__ = ('celery_app',)  # Define what is imported when * is used
