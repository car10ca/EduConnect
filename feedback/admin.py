from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Feedback model.
    Customizes the admin interface for managing feedback entries.
    """
    # Define which fields are displayed in the list view
    list_display = ('course', 'student', 'rating', 'date_posted', 'comment')
    
    # Add filters for easier navigation and data segmentation
    list_filter = ('rating', 'course', 'date_posted')
    
    # Add search functionality based on student username and course title
    search_fields = ('student__username', 'course__title')
    
    # Enable ordering by date posted (most recent first) and then by rating
    ordering = ('-date_posted', 'rating')
    
    # Make the 'rating' field editable directly in the list view
    list_editable = ('rating',)

    # Add a date hierarchy for easy date-based navigation
    date_hierarchy = 'date_posted'

    # Configure readonly fields to prevent unauthorized editing
    readonly_fields = ('date_posted',)

    # Organize the detail view with fieldsets for better layout
    fieldsets = (
        (None, {
            'fields': ('course', 'student', 'rating', 'comment')  # General feedback details
        }),
        ('Date Information', {
            'fields': ('date_posted',),  # Date-related information
        }),
    )
