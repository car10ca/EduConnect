from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """
    Configuration class for the Feedback app.
    Sets default settings and app-specific configurations.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField as the default auto field for primary keys
    name = 'feedback'  # Name of the app as used in Django's app registry
