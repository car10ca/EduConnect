# chat/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import ChatSession
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

@shared_task
def delete_expired_rooms():
    """
    Task to delete chat rooms that have expired.
    Runs as a scheduled task using Celery and checks for rooms where the expiry time has passed.
    """
    try:
        now = timezone.now()
        logger.info(f"Running delete_expired_rooms task at {now}.")  # Log the current time when the task runs

        # Query for chat sessions that have expired
        expired_rooms = ChatSession.objects.filter(expiry_time__lt=now)
        expired_rooms_count = expired_rooms.count()

        # Log the number of expired rooms before deletion
        if expired_rooms_count > 0:
            logger.info(f"Deleting {expired_rooms_count} expired rooms.")

        # Delete the expired chat sessions
        expired_rooms.delete()

        # Log confirmation after deletion
        if expired_rooms_count > 0:
            logger.info(f"Deleted {expired_rooms_count} expired rooms successfully.")

        return f"Deleted {expired_rooms_count} expired rooms."
    
    except Exception as e:
        # Log any errors that occur during the task
        logger.error(f"Error deleting expired rooms: {str(e)}")
        return f"Error occurred: {str(e)}"
