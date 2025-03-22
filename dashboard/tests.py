from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from feedback.models import Feedback
from notifications.models import Notification
from dashboard.models import StatusUpdate  # Importing the StatusUpdate model

User = get_user_model()


class DashboardViewTests(TestCase):
    """Tests for the dashboard view."""

    def setUp(self):
        """Set up users, courses, feedback, and notifications for testing."""
        # Create a teacher and a student
        self.teacher = User.objects.create_user(username='teacher', password='pass123', is_teacher=True)
        self.student = User.objects.create_user(username='student', password='pass123', is_teacher=False)

        # Create a course for the teacher
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.teacher)

        # Enroll the student in the course
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)

        # Create feedback for the course
        self.feedback = Feedback.objects.create(course=self.course, student=self.student, rating=4, comment='Great course!')

        # Create notifications for both users
        self.teacher_notification = Notification.objects.create(user=self.teacher, message='New feedback received.')
        self.student_notification = Notification.objects.create(user=self.student, message='You have been enrolled in a course.')

    def test_dashboard_view_for_teacher(self):
        """Test the dashboard view for a teacher."""
        self.client.login(username='teacher', password='pass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)

        # Check that the teacher sees the course they created
        self.assertContains(response, 'Test Course')

        # Check that the feedback section is present
        self.assertContains(response, 'Feedback')

        # Check that the notification link is present
        self.assertContains(response, 'View Notifications')

        # Check that the teacher-specific content is present
        self.assertContains(response, 'Your Courses')

    def test_dashboard_view_for_student(self):
        """Test the dashboard view for a student."""
        self.client.login(username='student', password='pass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)

        # Check that the student sees the enrolled course
        self.assertContains(response, 'Test Course')

        # Check that the notification link is present
        self.assertContains(response, 'View Notifications')

        # Ensure that the student-specific content is displayed
        self.assertContains(response, 'Enrolled Courses')


class StatusUpdateTests(TestCase):
    """Tests for the status update feature."""

    def setUp(self):
        """Set up users and status updates for testing."""
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.status_update = StatusUpdate.objects.create(user=self.user, content="Initial status")  # Create a status update for the user

    def test_edit_status_view(self):
        """Test that a user can edit their own status update."""
        self.client.login(username='user1', password='pass123')
        url = reverse('dashboard:edit_status', args=[self.status_update.id])
        response = self.client.post(url, {'content': 'Updated status'})
        self.status_update.refresh_from_db()
        self.assertEqual(self.status_update.content, 'Updated status')
        self.assertRedirects(response, reverse('accounts:user_profile_with_id', args=[self.user.id]))

    def test_edit_status_view_forbidden(self):
        """Test that a user cannot edit another user's status update."""
        other_user = User.objects.create_user(username='user2', password='pass123')
        self.client.login(username='user2', password='pass123')
        url = reverse('dashboard:edit_status', args=[self.status_update.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Should return 404 as user2 cannot edit user1's status
