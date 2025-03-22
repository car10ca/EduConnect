from django.urls import path
from . import views

# Define the application namespace
app_name = 'courses'

# URL patterns for the courses app
urlpatterns = [
    path('', views.course_list, name='course_list'),  # List all courses
    path('<int:course_id>/', views.course_detail, name='course_detail'),  # Detail view of a specific course
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),  # Edit a specific course
    path('<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),  # Enroll in a specific course
    path('material/<int:material_id>/delete/', views.delete_material, name='delete_material'),  # Delete a specific material
    path('<int:course_id>/add_material/', views.add_material, name='add_material'),  # Add material to a specific course
    path('<int:course_id>/remove_student/<int:student_id>/', views.remove_student, name='remove_student'),  # Remove a student from a course
    path('<int:course_id>/block_student/<int:student_id>/', views.block_student, name='block_student'),  # Block a student from a course
    path('<int:course_id>/unblock_student/<int:student_id>/', views.unblock_student, name='unblock_student'),  # Unblock a student in a course
    path('create/', views.course_create, name='course_create'),  # Create a new course
    path('<int:course_id>/search/', views.search_users, name='search_users'),  # Search for users to enroll in a course
    path('enroll_user_in_course/<int:user_id>/', views.enroll_user_in_course, name='enroll_user_in_course'),  # Enroll a specific user in a course
    path('<int:course_id>/update/', views.edit_course, name='course_update'), # Update an existing course
    path('<int:course_id>/delete/', views.delete_course, name='course_delete'), # Delete an existing course
]
