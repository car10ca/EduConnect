from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    Customizes the admin interface for managing notification entries.
    """
    
    # Fields to display in the list view
    list_display = ('user', 'message', 'created_at', 'is_read', 'content_type', 'object_id')
    
    # Filters for easier navigation and data segmentation
    list_filter = ('is_read', 'created_at', 'content_type')
    
    # Search functionality based on user, message, and content type
    search_fields = ('user__username', 'message', 'content_type__model')
    
    # Default ordering of notifications (most recent first)
    ordering = ('-created_at',)

    def mark_notifications_as_read(self, request, queryset):
        """
        Custom admin action to mark selected notifications as read.
        """
        queryset.update(is_read=True)
        self.message_user(request, "Selected notifications have been marked as read.")
    mark_notifications_as_read.short_description = "Mark selected notifications as read"

    def mark_notifications_as_unread(self, request, queryset):
        """
        Custom admin action to mark selected notifications as unread.
        """
        queryset.update(is_read=False)
        self.message_user(request, "Selected notifications have been marked as unread.")
    mark_notifications_as_unread.short_description = "Mark selected notifications as unread"

    # Register custom actions
    actions = [mark_notifications_as_read, mark_notifications_as_unread]

# Register the Notification model with the custom admin configuration
admin.site.register(Notification, NotificationAdmin)
