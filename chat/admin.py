from django.contrib import admin
from .models import ChatSession, Message, ChatAccessAttempt


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """
    Admin interface options for the ChatSession model.
    Provides a customized view of chat sessions in the admin panel.
    """
    list_display = ('name', 'created_by', 'is_private', 'created_at', 'expiry_time')
    list_filter = ('is_private', 'created_at')
    search_fields = ('name', 'created_by__username')
    filter_horizontal = ('participants', 'allowed_users')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Message model.
    Provides a customized view of messages in the admin panel.
    """
    list_display = ('chat_session', 'user', 'timestamp', 'message_excerpt')
    list_filter = ('chat_session', 'timestamp')
    search_fields = ('user__username', 'message')
    ordering = ('-timestamp',)

    def message_excerpt(self, obj):
        """
        Returns the first 50 characters of the message for display purposes.
        This provides a quick overview of the message content in the admin panel.
        """
        return obj.message[:50]
    message_excerpt.short_description = 'Message Excerpt'


@admin.register(ChatAccessAttempt)
class ChatAccessAttemptAdmin(admin.ModelAdmin):
    """
    Admin interface options for the ChatAccessAttempt model.
    Provides a customized view of chat access attempts in the admin panel.
    """
    list_display = ('user', 'room_name', 'timestamp', 'success')
    list_filter = ('success', 'timestamp')
    search_fields = ('user__username', 'room_name')
    ordering = ('-timestamp',)
