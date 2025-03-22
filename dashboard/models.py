from django.db import models
from accounts.models import User


class StatusUpdate(models.Model):
    """
    Model representing a status update made by a user.
    Contains information about the user, the content of the update, and the timestamp of creation.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='status_updates'
    )  # Foreign key to the User model, with cascading delete
    content = models.TextField(max_length=250)  # Text content of the status update, limited to 250 characters
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the status update was created

    def __str__(self):
        """
        String representation of the StatusUpdate model.
        Returns a formatted string showing the username and timestamp of the status update.
        """
        return f"Status by {self.user.username} at {self.timestamp}"
