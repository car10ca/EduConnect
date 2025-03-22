from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    Configuration class for the 'chat' app.
    This class sets application-specific settings for the chat app.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default auto field type for primary keys
    name = 'chat'  # Name of the app
