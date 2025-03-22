from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Enrollment, CourseMaterial
from feedback.models import Feedback
from notifications.models import Notification
from .forms import StatusUpdateForm
from .models import StatusUpdate


@login_required
def dashboard(request):
    """
    Renders the dashboard view, displaying different content for teachers and students.
    Teachers see their created courses and feedback, while students see enrolled courses.
    """
    context = {
        'username': request.user.username,  # Store the current user's username
        'is_teacher': request.user.is_teacher,  # Check if the current user is a teacher
    }
    
    # Fetch unread and read notifications for the logged-in user
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    read_notifications = Notification.objects.filter(user=request.user, is_read=True)

    context['unread_notifications'] = unread_notifications
    context['read_notifications'] = read_notifications
    
    if request.user.is_teacher:
        # Fetch the courses created by the teacher
        created_courses = Course.objects.filter(teacher=request.user)
        context['created_courses'] = created_courses
        
        # Prepare feedback and materials for each course
        course_feedback = []
        for course in created_courses:
            feedbacks = Feedback.objects.filter(course=course)  # Feedback linked to the course
            materials = CourseMaterial.objects.filter(course=course)  # Materials linked to the course
            course_feedback.append({
                'course': course,
                'feedbacks': feedbacks,
                'materials': materials  # Include course materials in context
            })
        context['course_feedback'] = course_feedback
        
    else:
        # Fetch the courses the student is enrolled in
        enrolled_courses = Enrollment.objects.filter(student=request.user)
        context['enrolled_courses'] = enrolled_courses
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def edit_status(request, status_id):
    """
    Allows a user to edit their status update.
    """
    # Fetch the status update object or return a 404 if not found
    status_update = get_object_or_404(StatusUpdate, id=status_id, user=request.user)
    
    if request.method == 'POST':
        # If the request is a POST, bind the form with the POST data and the existing status update instance
        form = StatusUpdateForm(request.POST, instance=status_update)
        if form.is_valid():  # Validate the form data
            form.save()  # Save the updated status
            messages.success(request, "Your status update has been updated.")  # Success message
            return redirect('accounts:user_profile_with_id', user_id=request.user.id)  # Redirect to the user's profile
    else:
        # If the request is not POST, instantiate the form with the existing status update
        form = StatusUpdateForm(instance=status_update)
    
    return render(request, 'dashboard/edit_status.html', {'form': form})  # Render the form in the template
