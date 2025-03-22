from django.urls import path
from . import consumers

# Define WebSocket URL patterns for the chat app
websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]
