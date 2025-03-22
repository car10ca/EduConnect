from django.urls import path
from . import views

app_name = 'feedback'  # Define the app namespace for URL namespacing

urlpatterns = [
    path('submit/<int:course_id>/', views.submit_feedback, name='submit_feedback'),  # URL for submitting feedback for a specific course
    path('view/<int:course_id>/', views.view_feedback, name='view_feedback'),  # URL for viewing feedback for a specific course
    path('list/', views.feedback_list, name='feedback_list'),  # URL for viewing the list of all feedback
]
