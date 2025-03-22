from rest_framework import serializers
from .models import Course, CourseMaterial, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model. Provides details about the course.
    It includes teacher information to show who created the course.
    """
    teacher_username = serializers.ReadOnlyField(source='teacher.username')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_username', 'created_at']

class CourseMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for course materials. Used to fetch details about
    files associated with a course.
    """
    class Meta:
        model = CourseMaterial
        fields = ['id', 'course', 'title', 'file', 'uploaded_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model. Handles enrolling students
    in courses and fetching details about student enrollments.
    """
    student_username = serializers.ReadOnlyField(source='student.username')
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_username', 'course', 'course_title', 'enrolled_at', 'is_blocked', 'is_removed']
