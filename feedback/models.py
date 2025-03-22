from django.db import models
from django.conf import settings
from courses.models import Course

class Feedback(models.Model):
    """
    Model representing feedback for a course.
    Each feedback is linked to a course and a student, and includes a rating and an optional comment.
    """
    
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )  # Foreign key linking feedback to a course, with cascading delete
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='feedback'
    )  # Foreign key linking feedback to a student, with cascading delete
    
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], 
        default=0
    )  # Integer field for rating, with choices ranging from 1 to 5
    
    comment = models.TextField(
        blank=True, 
        null=True
    )  # Optional text field for additional comments
    
    date_posted = models.DateTimeField(
        auto_now_add=True
    )  # DateTime field to store the date and time feedback was posted

    def __str__(self):
        """
        String representation of the Feedback instance.
        Displays the username of the student and the title of the course.
        """
        return f"Feedback by {self.student.username} on {self.course.title}"
