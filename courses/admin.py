from django.contrib import admin
from .models import Course, CourseMaterial, Enrollment


class CourseMaterialInline(admin.TabularInline):
    """
    Inline admin interface for adding and editing course materials
    directly from the Course admin page.
    """
    model = CourseMaterial  # Model to be used inline
    extra = 1  # Number of empty forms to display for adding new materials


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Course model.
    Provides a customized view of courses in the admin panel.
    """
    list_display = ('title', 'teacher', 'created_at')  # Fields to display in the list view
    list_filter = ('teacher', 'created_at')  # Fields to filter the list view
    search_fields = ('title', 'teacher__username')  # Fields to search within the list view
    inlines = [CourseMaterialInline]  # Inline model to manage course materials within the course


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    """
    Admin interface options for the CourseMaterial model.
    Provides a customized view of course materials in the admin panel.
    """
    list_display = ('title', 'course', 'uploaded_at')  # Fields to display in the list view
    list_filter = ('course',)  # Fields to filter the list view
    search_fields = ('title', 'course__title')  # Fields to search within the list view


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Enrollment model.
    Provides a customized view of enrollments in the admin panel.
    """
    list_display = ('student', 'course', 'enrolled_at', 'is_blocked', 'is_removed')  # Fields to display in the list view
    list_filter = ('course', 'is_blocked', 'is_removed')  # Fields to filter the list view
    search_fields = ('student__username', 'course__title')  # Fields to search within the list view
    list_editable = ('is_blocked', 'is_removed')  # Fields that can be edited directly in the list view
