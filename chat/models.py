from django.db import models
from django.utils import timezone
from datetime import timedelta

def default_expiry_time():
    """
    Function to set the default expiry time for a chat session.
    Returns the current time plus one day.
    """
    return timezone.now() + timedelta(days=1)


class ChatSession(models.Model):
    """
    Model representing a chat session.
    Contains information about the chat room, its creator, participants, and expiry details.
    """
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )  # Unique name for the chat room
    created_by = models.ForeignKey(
        'accounts.User',
        related_name='created_chats',
        on_delete=models.CASCADE
    )  # User who created the chat
    participants = models.ManyToManyField(
        'accounts.User',
        related_name='chat_sessions',
        blank=True
    )  # Users who are participants in the chat
    is_private = models.BooleanField(default=False)  # Indicates if the chat room is private
    allowed_users = models.ManyToManyField(
        'accounts.User',
        related_name='allowed_chat_sessions',
        blank=True
    )  # Users allowed in a private chat
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of chat creation
    expiry_time = models.DateTimeField(null=True, blank=True)  # Expiry time for public/private rooms; can be None for predefined rooms

    def __str__(self):
        """
        String representation of the ChatSession model.
        Returns the type of chat (Private/Public) with its name and expiry time.
        """
        room_type = "Private" if self.is_private else "Public"
        return (
            f"{room_type} Chat '{self.name}' (expires at {self.expiry_time.strftime('%Y-%m-%d %H:%M:%S')})"
            if self.expiry_time else f"Chat {self.id}"
        )

    def save(self, *args, **kwargs):
        """
        Override the save method to handle expiry times for rooms.
        Predefined rooms should have no expiry time, while public and private rooms should have an expiry time.
        """
        predefined_rooms = ['students', 'teachers', 'teacher_student']

        # Only set expiry_time for non-predefined rooms
        if self.name not in predefined_rooms and not self.expiry_time:
            self.expiry_time = default_expiry_time()

        super().save(*args, **kwargs)

    class Meta:
        """
        Meta options for the ChatSession model.
        Defines ordering and verbose name settings.
        """
        ordering = ['-created_at']
        verbose_name = "Chat Session"
        verbose_name_plural = "Chat Sessions"


class Message(models.Model):
    """
    Model representing a message sent in a chat session.
    Contains the chat session reference, user, message content, and timestamp.
    """
    chat_session = models.ForeignKey(
        ChatSession,
        related_name='messages',
        on_delete=models.CASCADE
    )  # Reference to the associated chat session
    user = models.ForeignKey(
        'accounts.User',
        related_name='messages',
        on_delete=models.CASCADE
    )  # User who sent the message
    message = models.TextField()  # The message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the message was sent

    def __str__(self):
        """
        String representation of the Message model.
        Returns the timestamp and first 50 characters of the message.
        """
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.user.username}: {self.message[:50]}"

    class Meta:
        """
        Meta options for the Message model.
        Defines ordering and verbose name settings.
        """
        ordering = ['timestamp']
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class ChatAccessAttempt(models.Model):
    """
    Model representing an attempt to access a chat room.
    Contains the user, room name, timestamp, and whether the access was successful.
    """
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )  # User attempting to access the chat room
    room_name = models.CharField(max_length=255)  # Name of the chat room being accessed
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the access attempt
    success = models.BooleanField()  # Whether the access attempt was successful

    def __str__(self):
        """
        String representation of the ChatAccessAttempt model.
        Returns the status of the access attempt with user and room details.
        """
        status = "successful" if self.success else "denied"
        return (
            f"Access {status} for {self.user.username} to room '{self.room_name}' on "
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    class Meta:
        """
        Meta options for the ChatAccessAttempt model.
        Defines ordering, verbose name settings, and indexing options.
        """
        ordering = ['-timestamp']
        verbose_name = "Chat Access Attempt"
        verbose_name_plural = "Chat Access Attempts"
        indexes = [
            models.Index(fields=['user', 'room_name', 'timestamp']),
        ]
