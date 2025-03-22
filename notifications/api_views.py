from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListAPIView(generics.ListAPIView):
    """
    API view to list all notifications for the logged-in user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return notifications for the logged-in user.
        """
        return Notification.objects.filter(user=self.request.user)

class NotificationMarkAsReadAPIView(generics.UpdateAPIView):
    """
    API view to mark a notification as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.mark_as_read()
        return Response(status=status.HTTP_200_OK)

    def get_object(self):
        """
        Return the notification instance.
        """
        notification_id = self.kwargs['notification_id']
        return Notification.objects.get(id=notification_id, user=self.request.user)
