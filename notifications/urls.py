from django.urls import path
from . import views

# Define the application namespace
app_name = 'notifications'

# URL patterns for the notifications app
urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),  # List all notifications for the user
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),  # Mark a specific notification as read
    path('mark_as_unread/<int:notification_id>/', views.mark_as_unread, name='mark_as_unread'),  # Mark a specific notification as unread
    path('delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),  # Delete a specific notification
]
