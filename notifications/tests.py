from django.test import TestCase
from django.urls import reverse
from .models import Notification
from accounts.models import User

class NotificationModelTests(TestCase):
    """Tests for the Notification model."""

    def setUp(self):
        """Set up a user for testing notification model creation."""
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_create_notification(self):
        """Test creating a new notification."""
        notification = Notification.objects.create(user=self.user, message='Test notification')
        self.assertEqual(notification.user, self.user)
        self.assertFalse(notification.is_read)  # Ensure the notification is unread by default
        self.assertEqual(notification.message, 'Test notification')  # Check the message content

    def test_notification_str_representation(self):
        """Test the string representation of the notification."""
        notification = Notification.objects.create(user=self.user, message='Test notification')
        self.assertEqual(str(notification), f'Notification for {self.user.username}: {notification.message}')
        # Ensure the correct string representation, including the user and message

class NotificationsViewTests(TestCase):
    """Tests for the notifications views."""

    def setUp(self):
        """Create a user and login for testing notifications views."""
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')

    def test_notifications_list_view(self):
        """Test the notifications list view."""
        response = self.client.get(reverse('notifications:notifications_list'))
        self.assertEqual(response.status_code, 200)  # Ensure the view returns a 200 status code
        self.assertContains(response, 'No notifications to show.')  # Check for the empty notification message

    def test_notifications_list_with_notifications(self):
        """Test the notifications list view with some notifications."""
        Notification.objects.create(user=self.user, message='Test notification 1')
        Notification.objects.create(user=self.user, message='Test notification 2')
        response = self.client.get(reverse('notifications:notifications_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test notification 1')
        self.assertContains(response, 'Test notification 2')

    def test_mark_as_read_view(self):
        """Test marking a notification as read."""
        notification = Notification.objects.create(user=self.user, message='Test notification')
        response = self.client.get(reverse('notifications:mark_as_read', args=[notification.id]))
        notification.refresh_from_db()  # Refresh from the database to get the updated notification
        self.assertTrue(notification.is_read)  # Ensure the notification is marked as read
        self.assertRedirects(response, reverse('notifications:notifications_list'))  # Ensure redirection to the list view

    def test_mark_as_unread_view(self):
        """Test marking a notification as unread."""
        notification = Notification.objects.create(user=self.user, message='Test notification', is_read=True)
        response = self.client.get(reverse('notifications:mark_as_unread', args=[notification.id]))
        notification.refresh_from_db()
        self.assertFalse(notification.is_read)  # Ensure the notification is marked as unread
        self.assertRedirects(response, reverse('notifications:notifications_list'))

    def test_delete_notification_view(self):
        """Test deleting a notification."""
        notification = Notification.objects.create(user=self.user, message='Test notification')
        response = self.client.get(reverse('notifications:delete_notification', args=[notification.id]))
        self.assertFalse(Notification.objects.filter(id=notification.id).exists())  # Ensure the notification is deleted
        self.assertRedirects(response, reverse('notifications:notifications_list'))

    def test_user_cannot_interact_with_another_users_notification(self):
        """Test that a user cannot mark or delete another user's notification."""
        other_user = User.objects.create_user(username='otheruser', password='pass123')
        notification = Notification.objects.create(user=other_user, message='Other user notification')

        # Try marking another user's notification as read
        response = self.client.get(reverse('notifications:mark_as_read', args=[notification.id]))
        self.assertEqual(response.status_code, 404)  # Should return a 404 error as it doesn't exist for the logged-in user

        # Try marking another user's notification as unread
        response = self.client.get(reverse('notifications:mark_as_unread', args=[notification.id]))
        self.assertEqual(response.status_code, 404)  # Should return a 404 error

        # Try deleting another user's notification
        response = self.client.get(reverse('notifications:delete_notification', args=[notification.id]))
        self.assertEqual(response.status_code, 404)  # Should return a 404 error
