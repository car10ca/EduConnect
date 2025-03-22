from rest_framework import serializers
from .models import ChatSession, Message

class ChatSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatSession model. Handles chat room details,
    including participants and privacy settings.
    """
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = ChatSession
        fields = ['id', 'name', 'created_by', 'created_by_username', 'is_private', 'expiry_time', 'participants']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model. Used for handling messages in chat sessions.
    """
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Message
        fields = ['id', 'chat_session', 'user', 'user_username', 'message', 'timestamp']
