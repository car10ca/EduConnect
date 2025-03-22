from rest_framework import generics, permissions
from .models import ChatSession, Message
from .serializers import ChatSessionSerializer, MessageSerializer

class ChatSessionListAPIView(generics.ListAPIView):
    """
    API view to list chat sessions. Only authenticated users
    can access this view to see their chat sessions.
    """
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return chat sessions that the logged-in user is a participant of.
        """
        return ChatSession.objects.filter(participants=self.request.user)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list messages in a chat session and allow sending messages.
    Only participants of the chat session can access this view.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return messages for a specific chat session.
        """
        chat_session_id = self.kwargs['chat_session_id']
        chat_session = ChatSession.objects.get(id=chat_session_id)
        if self.request.user in chat_session.participants.all():
            return chat_session.messages.all()
        else:
            raise permissions.PermissionDenied("You are not a participant of this chat session.")

    def perform_create(self, serializer):
        """
        Assign the message to the logged-in user and chat session.
        """
        chat_session_id = self.kwargs['chat_session_id']
        chat_session = ChatSession.objects.get(id=chat_session_id)
        if self.request.user in chat_session.participants.all():
            serializer.save(user=self.request.user, chat_session=chat_session)
        else:
            raise permissions.PermissionDenied("You are not a participant of this chat session.")
