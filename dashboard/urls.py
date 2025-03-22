from django.urls import path
from .views import dashboard  # Import the dashboard view directly
from . import views  # Import all views from the current app

# Define the application namespace
app_name = 'dashboard'

# URL patterns for the dashboard app
urlpatterns = [
    path('', dashboard, name='dashboard'),  # URL for the dashboard home view
    path('edit_status/<int:status_id>/', views.edit_status, name='edit_status'),  # URL for editing a specific status update
]
