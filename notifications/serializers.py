from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model. Used to fetch notifications
    for users and manage notification states.
    """
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_username', 'message', 'created_at', 'is_read', 'content_type', 'object_id']
