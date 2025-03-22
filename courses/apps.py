from django.apps import AppConfig


class CoursesConfig(AppConfig):
    """
    Configuration class for the 'courses' app.
    This class sets application-specific settings for the courses app.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Default auto field type for primary keys
    name = 'courses'  # Name of the app
