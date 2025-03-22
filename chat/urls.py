from django.urls import path
from . import views

# Define the namespace for the chat app
app_name = 'chat'

# URL patterns for the chat app
urlpatterns = [
    path('', views.chat_home, name='chat_home'),  # Home page for chat, displays available rooms
    path('<str:room_name>/', views.room, name='room'),  # View for a specific chat room
    path('<str:room_name>/delete/', views.delete_room, name='delete_room'),  # View to delete a room, accessible only to the room creator
]
