from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL


class Course(models.Model):
    """
    Model representing a course.
    Contains information about the course title, description, teacher, creation date,
    and a list of students who are blocked from the course.
    """
    title = models.CharField(max_length=200)  # Title of the course
    description = models.TextField()  # Description of the course
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )  # Foreign key to the user who is the teacher of the course
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the course was created
    blocked_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='blocked_courses',
        blank=True
    )  # Many-to-many relationship with users who are blocked from the course

    def __str__(self):
        """
        String representation of the Course model.
        Returns the course title.
        """
        return self.title


class CourseMaterial(models.Model):
    """
    Model representing a material or resource for a course.
    Contains information about the course it belongs to, the title, the file itself, and the upload date.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )  # Foreign key to the course this material is related to
    title = models.CharField(max_length=200)  # Title of the course material
    file = models.FileField(upload_to='course_materials/')  # File associated with the material
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the material was uploaded

    def __str__(self):
        """
        String representation of the CourseMaterial model.
        Returns the title of the material and the course it belongs to.
        """
        return f"Material: {self.title} for Course: {self.course.title}"


class Enrollment(models.Model):
    """
    Model representing the enrollment of a student in a course.
    Contains information about the student, the course, enrollment date, and status flags for blocking and removal.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )  # Foreign key to the user who is enrolled in the course
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )  # Foreign key to the course in which the student is enrolled
    enrolled_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the enrollment was made
    is_blocked = models.BooleanField(default=False)  # Flag indicating if the student is blocked from the course
    is_removed = models.BooleanField(default=False)  # Flag indicating if the student has been removed from the course

    class Meta:
        unique_together = ('student', 'course')  # Ensures that each student can only enroll in a course once

    def __str__(self):
        """
        String representation of the Enrollment model.
        Returns a string showing the student's username and the course title.
        """
        return f"{self.student.username} enrolled in {self.course.title}"