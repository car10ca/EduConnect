import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Set the default settings module for the 'asgi' application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduConnect.settings')

# Setup Django ASGI application
django_asgi_app = get_asgi_application()

# Import the routing configuration after apps are loaded
import chat.routing  # Import the routing configuration from the chat app

# Define the application routing with Channels
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Handle traditional HTTP requests with Django
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # Route WebSocket requests to chat app
        )
    ),
})
