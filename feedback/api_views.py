from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer
from courses.models import Course

class FeedbackListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all feedback for a specific course and allow students
    to submit feedback. Only students enrolled in the course can submit feedback.
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter feedback by course ID.
        """
        course_id = self.kwargs['course_id']
        return Feedback.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        """
        Check if the student is enrolled in the course before allowing feedback.
        """
        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)
        if not course.enrollments.filter(student=self.request.user).exists():
            raise permissions.PermissionDenied("You must be enrolled in this course to provide feedback.")
        serializer.save(course=course, student=self.request.user)
