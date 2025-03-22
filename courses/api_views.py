from rest_framework import generics, permissions
from .models import Course, CourseMaterial, Enrollment
from .serializers import CourseSerializer, CourseMaterialSerializer, EnrollmentSerializer

class CourseListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all courses and allow teachers to create new courses.
    Only authenticated users can access this view.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the teacher to the currently logged-in user when creating a course.
        """
        serializer.save(teacher=self.request.user)

class EnrollmentAPIView(generics.CreateAPIView):
    """
    API view to handle student enrollment in a course.
    Only students can enroll in courses.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the student to the currently logged-in user.
        """
        serializer.save(student=self.request.user)

class CourseMaterialListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list and create course materials.
    Only the course teacher can add materials.
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the course for the material and assign the uploaded material to it.
        """
        course_id = self.request.data.get('course')
        course = Course.objects.get(id=course_id)
        if self.request.user == course.teacher:
            serializer.save(course=course)
        else:
            raise permissions.PermissionDenied("You do not have permission to add materials to this course.")
