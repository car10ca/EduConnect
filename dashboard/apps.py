from django.apps import AppConfig


class DashboardConfig(AppConfig):
    """
    Configuration class for the 'dashboard' app.
    This class sets application-specific settings for the dashboard app.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default auto field type for primary keys
    name = 'dashboard'  # Name of the app
