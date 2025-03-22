from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Get the user model used in the project (custom or default)
User = get_user_model()

# Defines the Notification model to manage notifications for users
class Notification(models.Model):
    """
    Model to represent notifications for users.
    Each notification is linked to a user and may be related to other content in the system using generic relations.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )  # The user who receives the notification

    message = models.TextField()  # The message content of the notification

    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the notification was created

    is_read = models.BooleanField(default=False)  # Status to check if the notification has been read

    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )  # Generic foreign key to associate notification with any model

    object_id = models.PositiveIntegerField(
        null=True, 
        blank=True
    )  # ID of the related object

    content_object = GenericForeignKey('content_type', 'object_id')  # Combines content_type and object_id to create a generic relation

    def __str__(self):
        """
        String representation of the Notification model.
        """
        return f"Notification for {self.user.username}: {self.message}"

    def mark_as_read(self):
        """
        Marks the notification as read and saves the change.
        """
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        """
        Marks the notification as unread and saves the change.
        """
        self.is_read = False
        self.save()
