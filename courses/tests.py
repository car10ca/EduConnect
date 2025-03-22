from django.test import TestCase
from django.urls import reverse
from .models import Course, Enrollment
from accounts.models import User
from django.core.exceptions import PermissionDenied

class CourseModelTests(TestCase):
    """Tests for the Course model."""

    def setUp(self):
        """Set up a teacher user and a course for testing."""
        self.teacher = User.objects.create_user(username='teacher', password='pass123', is_teacher=True)

    def test_create_course(self):
        """Test creating a new course."""
        course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.teacher)
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.teacher.username, 'teacher')

    def test_course_str_representation(self):
        """Test the string representation of a course."""
        course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.teacher)
        self.assertEqual(str(course), 'Test Course')

class EnrollmentTests(TestCase):
    """Tests for student enrollment in courses."""

    def setUp(self):
        """Set up a student, a teacher, and a course for testing enrollments."""
        self.student = User.objects.create_user(username='student', password='pass123', is_teacher=False)
        self.teacher = User.objects.create_user(username='teacher', password='pass123', is_teacher=True)
        self.course = Course.objects.create(title='Test Course', description='Test Description', teacher=self.teacher)

    def test_enroll_student(self):
        """Test enrolling a student in a course."""
        enrollment = Enrollment.objects.create(student=self.student, course=self.course)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_enroll_student_view(self):
        """Test the enrollment view for a student."""
        self.client.login(username='student', password='pass123')
        response = self.client.post(reverse('courses:enroll_in_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_prevent_duplicate_enrollment(self):
        """Test that a student cannot enroll twice in the same course."""
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=self.student, course=self.course)  # Should raise an IntegrityError

class CourseCreateViewTests(TestCase):
    """Tests for the course creation view."""

    def setUp(self):
        """Set up a teacher user for testing course creation."""
        self.teacher = User.objects.create_user(username='teacher_test', password='password123', is_teacher=True)
        self.client.login(username='teacher_test', password='password123')

    def test_create_course_view(self):
        """
        Test the course creation view for a teacher.
        Ensure that submitting valid form data redirects to the course detail page.
        """
        url = reverse('courses:course_create')
        form_data = {
            'title': 'New Test Course',
            'description': 'This is a test course description.'
        }
        formset_data = {
            'materials-TOTAL_FORMS': '1',
            'materials-INITIAL_FORMS': '0',
            'materials-0-title': 'Test Material',
            'materials-0-file': '',  # Optional: no file uploaded
        }
        data = {**form_data, **formset_data}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)  # Check if redirect happened after successful form submission
        self.assertTrue(Course.objects.filter(title='New Test Course').exists())

    def test_create_course_view_forbidden_for_non_teachers(self):
        """Test that non-teachers cannot create a course."""
        non_teacher = User.objects.create_user(username='student_test', password='password123', is_teacher=False)
        self.client.login(username='student_test', password='password123')
        response = self.client.get(reverse('courses:course_create'))
        self.assertEqual(response.status_code, 403)  # Forbidden access

class CourseUpdateViewTests(TestCase):
    """Tests for updating a course."""

    def setUp(self):
        """Set up a teacher and a course for testing updates."""
        self.teacher = User.objects.create_user(username='teacher_update', password='password123', is_teacher=True)
        self.course = Course.objects.create(title='Old Course', description='Old Description', teacher=self.teacher)
        self.client.login(username='teacher_update', password='password123')

    def test_update_course_view(self):
        """Test updating a course by the teacher who created it."""
        url = reverse('courses:course_update', args=[self.course.id])
        data = {
            'title': 'Updated Course Title',
            'description': 'Updated Course Description',
            # Management form data for the inline formset
            'materials-TOTAL_FORMS': '1',
            'materials-INITIAL_FORMS': '0',
            'materials-MIN_NUM_FORMS': '0',
            'materials-MAX_NUM_FORMS': '1000',
            'materials-0-title': 'Test Material',
            'materials-0-file': '',  # No file in this test case
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect on success
        self.course.refresh_from_db()  # Refresh the course object from the database
        self.assertEqual(self.course.title, 'Updated Course Title')
        self.assertEqual(self.course.description, 'Updated Course Description')

    def test_update_course_view_forbidden_for_non_teachers(self):
        """Test that non-teachers cannot update a course."""
        non_teacher = User.objects.create_user(username='student_test', password='password123', is_teacher=False)
        self.client.login(username='student_test', password='password123')
        url = reverse('courses:course_update', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # Expect Forbidden access


class CourseDeleteViewTests(TestCase):
    """Tests for deleting a course."""

    def setUp(self):
        """Set up a teacher and a course for testing deletion."""
        self.teacher = User.objects.create_user(username='teacher_delete', password='password123', is_teacher=True)
        self.course = Course.objects.create(title='Course to Delete', description='Delete Me', teacher=self.teacher)
        self.client.login(username='teacher_delete', password='password123')

    def test_delete_course_view(self):
        """Test that a teacher can delete their course."""
        url = reverse('courses:course_delete', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Check if redirect happened after deletion
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_delete_course_forbidden_for_non_teachers(self):
        """
        Test that non-teachers cannot delete a course.
        """
        non_teacher = User.objects.create_user(username='student_test', password='password123', is_teacher=False)
        self.client.login(username='student_test', password='password123')
        response = self.client.post(reverse('courses:course_delete', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)  # Expect Forbidden access

class CourseListViewTests(TestCase):
    """Tests for the course list view."""

    def setUp(self):
        """Set up multiple courses for testing the list view."""
        self.teacher = User.objects.create_user(username='teacher_list', password='password123', is_teacher=True)
        self.client.login(username='teacher_list', password='password123')  # Ensure the user is logged in
        self.course1 = Course.objects.create(title='Course 1', description='Description 1', teacher=self.teacher)
        self.course2 = Course.objects.create(title='Course 2', description='Description 2', teacher=self.teacher)

    def test_course_list_view(self):
        """Test that the course list view shows all courses."""
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK response
        self.assertContains(response, 'Course 1')
        self.assertContains(response, 'Course 2')

    def test_course_list_view_pagination(self):
        """Test that the course list view has pagination."""
        response = self.client.get(reverse('courses:course_list'), {'page': 1})
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK response
        self.assertTrue('is_paginated' in response.context)
