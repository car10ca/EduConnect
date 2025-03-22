from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    """
    Configuration class for the Notifications app.
    Sets default settings and handles app-specific setup.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField as the default auto field for primary keys
    name = 'notifications'  # Name of the app as used in Django's app registry

    def ready(self):
        """
        Override the ready method to import signal handlers.
        This ensures that signals are connected when the app is ready.
        """
        import notifications.signals  # Import the signals to connect them
