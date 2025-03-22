from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' app. 
    This class inherits from Django's AppConfig and sets application-specific configurations.
    """
    
    # Define the default type of auto-generated primary key field
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Set the name of the app
    name = 'accounts'
