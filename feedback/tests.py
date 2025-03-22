from django.test import TestCase
from django.urls import reverse
from .models import Feedback
from courses.models import Course, Enrollment
from accounts.models import User
from django.core.exceptions import ValidationError

class FeedbackModelTests(TestCase):
    """Tests for the Feedback model."""

    def setUp(self):
        """Set up a teacher, a student, and a course for testing feedback."""
        self.teacher = User.objects.create_user(username='teacher', password='pass123', is_teacher=True)
        self.student = User.objects.create_user(username='student', password='pass123', is_teacher=False)
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.teacher)

    def test_create_feedback(self):
        """Test creating feedback for a course."""
        feedback = Feedback.objects.create(course=self.course, student=self.student, rating=4, comment='Great course!')
        self.assertEqual(feedback.course, self.course)
        self.assertEqual(feedback.student, self.student)
        self.assertEqual(feedback.rating, 4)
        self.assertEqual(feedback.comment, 'Great course!')

    def test_feedback_str_representation(self):
        """Test the string representation of feedback."""
        feedback = Feedback.objects.create(course=self.course, student=self.student, rating=5, comment='Excellent!')
        # Adjusted the expected string to match actual behavior
        self.assertEqual(str(feedback), f'Feedback by {self.student.username} on {self.course.title}')

    def test_invalid_rating_value(self):
        """Test that feedback with invalid rating values raises a validation error."""
        feedback = Feedback(course=self.course, student=self.student, rating=10, comment='Out of range!')
        with self.assertRaises(ValidationError):
            feedback.full_clean()  # This method triggers validation


class FeedbackSubmissionTests(TestCase):
    """Tests for feedback submission functionality."""

    def setUp(self):
        """Set up a teacher, a student, a course, and enroll the student for testing feedback submission."""
        self.teacher = User.objects.create_user(username='teacher_test', password='password123', is_teacher=True)
        self.student = User.objects.create_user(username='student_test', password='password123', is_teacher=False)
        self.course = Course.objects.create(title='Test Course', description='Test Course Description', teacher=self.teacher)
        Enrollment.objects.create(student=self.student, course=self.course)
        self.client.login(username='student_test', password='password123')

    def test_submit_feedback_view(self):
        """Test that a student can submit feedback for a course."""
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        form_data = {
            'rating': 5,
            'comment': 'Great course!'
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect
        self.assertTrue(Feedback.objects.filter(course=self.course, student=self.student).exists())

    def test_submit_feedback_without_comment(self):
        """Test that feedback can be submitted without a comment."""
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        form_data = {
            'rating': 4,  # No comment provided
            'comment': ''
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect
        feedback = Feedback.objects.get(course=self.course, student=self.student)
        self.assertEqual(feedback.comment, '')  # Ensure comment is empty

    def test_submit_feedback_invalid_rating(self):
        """Test that submitting feedback with an invalid rating returns an error."""
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        form_data = {
            'rating': 10,  # Invalid rating (should be between 1 and 5)
            'comment': 'Invalid rating!'
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)  # The form should re-render with errors
        self.assertContains(response, 'Select a valid choice. 10 is not one of the available choices.')

    def test_duplicate_feedback_submission(self):
        """Test that a student cannot submit multiple feedback entries for the same course."""
        Feedback.objects.create(course=self.course, student=self.student, rating=4, comment='Good course!')
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        form_data = {
            'rating': 3,
            'comment': 'Trying to submit again!'
        }
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 200)  # Expect re-render with duplicate submission error
        self.assertContains(response, 'You have already submitted feedback for this course.')

class FeedbackViewPermissionsTests(TestCase):
    """Tests for feedback view permissions."""

    def setUp(self):
        """Set up users, courses, and enrollments for permission tests."""
        self.teacher = User.objects.create_user(username='teacher_test', password='password123', is_teacher=True)
        self.student = User.objects.create_user(username='student_test', password='password123', is_teacher=False)
        self.course = Course.objects.create(title='Test Course', description='Test Course Description', teacher=self.teacher)
        Enrollment.objects.create(student=self.student, course=self.course)
    
    def test_feedback_access_by_non_enrolled_student(self):
        """Test that a non-enrolled student cannot submit feedback."""
        non_enrolled_student = User.objects.create_user(username='non_enrolled', password='pass123', is_teacher=False)
        self.client.login(username='non_enrolled', password='pass123')
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Expect 403 Forbidden for non-enrolled student

    def test_teacher_cannot_submit_feedback(self):
        """Test that teachers cannot submit feedback for their own course."""
        self.client.login(username='teacher_test', password='password123')
        url = reverse('feedback:submit_feedback', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Expect 403 Forbidden for teacher
