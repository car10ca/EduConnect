from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm
from courses.models import Course
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden


@login_required
def submit_feedback(request, course_id=None):
    """
    Allows a student to submit feedback for a specific course or view a list of courses where feedback can be submitted.
    """
    if course_id:
        # Submitting feedback for a specific course
        course = get_object_or_404(Course, id=course_id)
        # Ensure the student is enrolled in the course
        if not course.enrollments.filter(student=request.user).exists():
            return HttpResponseForbidden()

        # Check if feedback has already been submitted
        if Feedback.objects.filter(course=course, student=request.user).exists():
            error_message = 'You have already submitted feedback for this course.'
            return render(request, 'feedback/submit_feedback.html', {
                'course': course,
                'error_message': error_message,
                'form': None
            })

        # Process feedback submission
        if request.method == 'POST':
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save(commit=False)
                feedback.course = course
                feedback.student = request.user
                feedback.save()
                return redirect('courses:course_detail', course_id=course.id)
        else:
            form = FeedbackForm()

        return render(request, 'feedback/submit_feedback.html', {'form': form, 'course': course})

    else:
        # Show list of courses where feedback can be submitted
        enrollments = request.user.enrollments.all()
        course_feedback_status = [
            {
                'course': enrollment.course,
                'has_given_feedback': Feedback.objects.filter(course=enrollment.course, student=request.user).exists()
            }
            for enrollment in enrollments
        ]
        return render(request, 'feedback/submit_feedback.html', {'course_feedback_status': course_feedback_status})


@login_required
def view_feedback(request, course_id):
    """
    Allows the teacher of a course to view all feedback provided for that course.
    Only the teacher of the course can view the feedback.
    """
    course = get_object_or_404(Course, id=course_id)

    # Redirect if the current user is not the teacher of the course
    if request.user != course.teacher:
        raise PermissionDenied()  # Return 403 Forbidden if the user is not the course teacher

    feedback_list = course.feedback.all()  # Retrieve all feedback related to the course
    return render(request, 'feedback/view_feedback.html', {'course': course, 'feedback_list': feedback_list})


@login_required
def feedback_list(request):
    """
    View to display either all feedback for teachers or the list of enrolled courses 
    for students to submit feedback.
    Implements pagination for teachers, and orders feedback by most recent.
    """
    if request.user.is_teacher:
        # Teachers should see all feedback entries for their courses, ordered by most recent first
        feedbacks = Feedback.objects.filter(course__teacher=request.user).order_by('-date_posted')
        
        # Pagination: show 10 feedbacks per page
        paginator = Paginator(feedbacks, 10)  # 10 feedbacks per page
        page_number = request.GET.get('page')  # Get the page number from the request
        page_obj = paginator.get_page(page_number)  # Get the feedbacks for the current page

        return render(request, 'feedback/feedback_list.html', {
            'page_obj': page_obj,  # Pass the paginated feedbacks
        })
    else:
        # Students should see their enrolled courses and the option to submit feedback
        enrollments = request.user.enrollments.all()  # Get all courses the student is enrolled in
        course_feedback_status = [
            {
                'course': enrollment.course,
                'has_given_feedback': Feedback.objects.filter(course=enrollment.course, student=request.user).exists()
            }
            for enrollment in enrollments
        ]
        return render(request, 'feedback/submit_feedback.html', {'course_feedback_status': course_feedback_status})