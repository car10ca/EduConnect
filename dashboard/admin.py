from django.contrib import admin
from .models import StatusUpdate


@admin.register(StatusUpdate)
class StatusUpdateAdmin(admin.ModelAdmin):
    """
    Admin interface options for the StatusUpdate model.
    Provides a customized view of status updates in the admin panel.
    """
    list_display = ('user', 'content', 'timestamp')  # Fields to display in the list view
    search_fields = ('user__username', 'content')  # Fields to search within the list view
    list_filter = ('timestamp',)  # Fields to filter the list view
    ordering = ('-timestamp',)  # Default ordering of the list view, descending by timestamp
