from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for Feedback model. Handles the submission and display
    of feedback related to courses.
    """
    student_username = serializers.ReadOnlyField(source='student.username')
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Feedback
        fields = ['id', 'course', 'course_title', 'student', 'student_username', 'rating', 'comment', 'date_posted']
