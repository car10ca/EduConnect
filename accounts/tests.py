from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for the User model."""

    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_teacher(self):
        """Test creating a new teacher user."""
        teacher = User.objects.create_user(username='testteacher', password='testpass123', is_teacher=True)
        self.assertTrue(teacher.is_teacher)


class UserRegistrationViewTests(TestCase):
    """Tests for the user registration view."""

    def setUp(self):
        """Set up test users."""
        self.teacher_group = Group.objects.create(name='Teachers')
        self.student_group = Group.objects.create(name='Students')

    def test_register_user_view(self):
        """Test registering a new user via the registration view."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'is_teacher': False
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_without_username(self):
        """Test registering without providing a username."""
        response = self.client.post(reverse('accounts:register'), {
            'email': 'user@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'is_teacher': False
        })
        self.assertEqual(response.status_code, 200)  # Should remain on the registration page
        self.assertContains(response, 'This field is required.')  # Check for form error

    def test_register_user_with_mismatched_passwords(self):
        """Test registering with mismatched passwords."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'user@test.com',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'is_teacher': False
        })
        self.assertEqual(response.status_code, 200)  # Should remain on the registration page
        self.assertContains(response, 'The two password fields didn’t match.')  # Check for password mismatch error

    def test_register_teacher(self):
        """Test registering a new teacher user."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'teacheruser',
            'email': 'teacheruser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'is_teacher': True
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        teacher = User.objects.get(username='teacheruser')
        self.assertTrue(teacher.is_teacher)  # Ensure user is registered as a teacher
        self.assertTrue(teacher.groups.filter(name='Teachers').exists())  # Check that the teacher group was assigned

    def test_register_student(self):
        """Test registering a new student user."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'studentuser',
            'email': 'studentuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'is_teacher': False
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration
        student = User.objects.get(username='studentuser')
        self.assertFalse(student.is_teacher)  # Ensure user is registered as a student
        self.assertTrue(student.groups.filter(name='Students').exists())  # Check that the student group was assigned


class UserProfileViewTests(TestCase):
    """Tests for the user profile view."""

    def setUp(self):
        """Create a user for testing the profile view."""
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_profile_view(self):
        """Test the user profile page loads correctly for a logged-in user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_profile_view_requires_login(self):
        """Test that the user profile page requires login."""
        response = self.client.get(reverse('accounts:user_profile'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_view_another_user_profile(self):
        """Test viewing another user's profile."""
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:user_profile_with_id', args=[self.other_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'otheruser')


class EditProfileViewTests(TestCase):
    """Tests for the profile editing view."""

    def setUp(self):
        """Create a user for testing the edit profile view."""
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_edit_profile_view(self):
        """Test editing the user profile."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('accounts:edit_profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful profile update
        self.user.refresh_from_db()  # Reload user from the database
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_edit_profile_requires_login(self):
        """Test that the edit profile page requires login."""
        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
