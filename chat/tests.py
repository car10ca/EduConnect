from django.test import TestCase
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from .models import ChatSession, Message, ChatAccessAttempt
from accounts.models import User
from EduConnect.asgi import application
from django.core.exceptions import PermissionDenied


class ChatModelTests(TestCase):
    """Tests for the ChatSession and Message models."""

    def test_create_chat_session(self):
        """Test creating a new chat session."""
        user = User.objects.create_user(username='user1', password='pass123')
        chat_session = ChatSession.objects.create(name='Test Room', created_by=user)
        self.assertEqual(chat_session.name, 'Test Room')
        self.assertEqual(chat_session.created_by, user)

    def test_create_message(self):
        """Test sending a message in a chat session."""
        user = User.objects.create_user(username='user1', password='pass123')
        chat_session = ChatSession.objects.create(name='Test Room', created_by=user)
        message = Message.objects.create(chat_session=chat_session, user=user, message='Hello')
        self.assertEqual(message.message, 'Hello')
        self.assertEqual(message.user, user)

    def test_delete_chat_session(self):
        """Test deleting a chat session."""
        user = User.objects.create_user(username='user1', password='pass123')
        chat_session = ChatSession.objects.create(name='Test Room', created_by=user)
        chat_session.delete()
        self.assertFalse(ChatSession.objects.filter(name='Test Room').exists())


class ChatWebSocketTests(TestCase):
    """Tests for WebSocket communication in chat sessions."""

    async def test_chat_websocket(self):
        """Test WebSocket connection for chat."""
        communicator = WebsocketCommunicator(application, "/ws/chat/TestRoom/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_websocket_message_sending(self):
        """Test WebSocket message sending and receiving."""
        communicator = WebsocketCommunicator(application, "/ws/chat/TestRoom/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send a message through the WebSocket
        await communicator.send_json_to({
            'message': 'Hello!',
            'username': 'user1',
            'room': 'TestRoom',
        })

        # Check if the message is received
        response = await communicator.receive_json_from()
        self.assertEqual(response['message'], 'Hello!')
        self.assertEqual(response['username'], 'user1')

        await communicator.disconnect()


class ChatAccessTests(TestCase):
    """Tests for accessing chat rooms and view permissions."""

    def setUp(self):
        """Set up users, chat session, and groups for testing."""
        self.teacher = User.objects.create_user(username='teacher1', password='pass123', is_teacher=True)
        self.student = User.objects.create_user(username='student1', password='pass123')
        self.chat_session = ChatSession.objects.create(name='Test Room', created_by=self.teacher)

    def test_join_chat_room_view(self):
        """Test joining a chat room as a logged-in user."""
        self.client.login(username='student1', password='pass123')
        response = self.client.get(reverse('chat:room', args=[self.chat_session.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Room')

    def test_access_private_room_denied(self):
        """Test that a user is denied access to a private room if they are not allowed."""
        # Create a private room, only allowing the teacher to access it
        private_room = ChatSession.objects.create(name='Private Room', created_by=self.teacher, is_private=True)
        private_room.allowed_users.add(self.teacher)  # Only the teacher is allowed

        # Log in as the student (who should not have access)
        self.client.login(username='student1', password='pass123')

        # Attempt to access the private room
        response = self.client.get(reverse('chat:room', args=[private_room.name]))

        # Ensure that access is denied and the correct status code (403) is returned
        self.assertEqual(response.status_code, 403)

    def test_access_private_room_allowed(self):
        """Test access granted to a private room for an allowed user."""
        self.chat_session.is_private = True
        self.chat_session.allowed_users.add(self.student)  # Add student to allowed users
        self.chat_session.save()

        # Join the private room as an allowed student
        self.client.login(username='student1', password='pass123')
        response = self.client.get(reverse('chat:room', args=[self.chat_session.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Room')

    def test_delete_room_view(self):
        """Test deleting a chat room by the creator."""
        self.client.login(username='teacher1', password='pass123')
        response = self.client.post(reverse('chat:delete_room', args=[self.chat_session.name]))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful deletion
        self.assertFalse(ChatSession.objects.filter(name='Test Room').exists())

    def test_delete_room_denied_for_non_creator(self):
        """Test that a non-creator cannot delete a chat room."""
        # Log in as the student (non-creator)
        self.client.login(username='student1', password='pass123')

        # Try to delete the room created by the teacher
        response = self.client.post(reverse('chat:delete_room', args=[self.chat_session.name]))

        # Ensure that access is denied (403 Forbidden)
        self.assertEqual(response.status_code, 403)

    def test_access_students_only_room_denied(self):
        """Test that non-students cannot access the students-only room."""
        self.client.login(username='teacher1', password='pass123')  # Log in as a teacher (not a student)
        response = self.client.get(reverse('chat:room', args=['students']))
        self.assertEqual(response.status_code, 403)  # Expecting 403 Forbidden for non-students

    def test_access_teachers_only_room_denied(self):
        """Test that non-teachers cannot access the teachers-only room."""
        self.client.login(username='student1', password='pass123')  # Log in as a student (not a teacher)
        response = self.client.get(reverse('chat:room', args=['teachers']))
        self.assertEqual(response.status_code, 403)  # Expecting 403 Forbidden for non-teachers

    def test_access_teacher_student_room_allowed(self):
        """Test access allowed for the teacher-student room."""
        chat_session = ChatSession.objects.create(name='teacher_student', created_by=self.teacher)
        self.client.login(username='student1', password='pass123')
        response = self.client.get(reverse('chat:room', args=['teacher_student']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'teacher_student')

    def test_create_room(self):
        """Test creating a new chat room."""
        response = self.client.post(reverse('chat:chat_home'), {
            'name': 'New Room',
            'is_private': False,
            'allowed_users': [self.teacher.id]
        })

        # Check if form is valid and print any form errors for debugging
        if response.context and 'form' in response.context:
            form = response.context['form']
            if not form.is_valid():
                print(form.errors)  # This will help identify any form issues

        self.assertEqual(response.status_code, 302)

    def test_create_room_missing_name(self):
        """Test creating a new room without a name."""
        self.client.login(username='teacher1', password='pass123')

        # Post with missing room name
        response = self.client.post(reverse('chat:chat_home'), {
            'name': '',
            'is_private': False,
            'allowed_users': []
        })

        # The form should return an error message and not redirect
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Room name cannot be empty.")
