from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Course, Enrollment, CourseMaterial
from .forms import CourseForm, CourseMaterialForm
from notifications.custom_signals import (
    student_blocked, student_unblocked, student_unenrolled, student_enrolled
)
import logging

# Configure a logger for debugging purposes
logger = logging.getLogger(__name__)
User = get_user_model()

@login_required
def course_list(request):
    """
    Display a list of courses.
    Teachers see their created courses; students see available and enrolled courses.
    Includes pagination for both views and applies ordering to avoid pagination inconsistencies.
    """
    if request.user.is_teacher:
        # Fetch all courses created by the teacher
        courses = Course.objects.filter(teacher=request.user).order_by('title')

        # Debugging: log number of courses and the actual courses
        logger.debug(f"Teacher {request.user.username} has created {courses.count()} courses.")
        logger.debug(f"Courses for {request.user.username}: {list(courses.values('title', 'id'))}")  # Log course titles and IDs

        # Paginate courses for teachers
        paginator = Paginator(courses, 10)  # 10 courses per page
        page_number = request.GET.get('page')
        courses_page = paginator.get_page(page_number)

        # Render the course list template for teachers
        return render(request, 'courses/course_list.html', {
            'courses': courses_page,
            'is_paginated': courses_page.has_other_pages(),
        })

    else:
        # Student view: show enrolled, available, and unavailable courses
        all_courses = Course.objects.all().distinct().order_by('title')  # Fetch all courses
        enrolled_courses = Enrollment.objects.filter(
            student=request.user, is_removed=False, is_blocked=False
        ).select_related('course').distinct().order_by('course__title')  # Fetch enrolled courses

        # Get the list of course IDs the student is already enrolled in
        enrolled_course_ids = enrolled_courses.values_list('course__id', flat=True)

        # Fetch unavailable courses (blocked or removed from enrollment)
        unavailable_courses = Course.objects.filter(
            Q(enrollments__student=request.user, enrollments__is_removed=True) |
            Q(enrollments__student=request.user, enrollments__is_blocked=True)
        ).distinct().order_by('title')

        # Available courses: exclude courses the student is already enrolled in or blocked from
        available_courses = all_courses.exclude(
            id__in=enrolled_course_ids
        ).exclude(id__in=unavailable_courses.values_list('id', flat=True)).distinct()

        # Paginate available courses for students
        paginator = Paginator(available_courses, 10)
        page_number = request.GET.get('page')
        available_courses_page = paginator.get_page(page_number)

        context = {
            'available_courses': available_courses_page,
            'enrolled_courses': enrolled_courses,
            'unavailable_courses': unavailable_courses,
            'is_paginated': available_courses_page.has_other_pages(),
        }
        return render(request, 'courses/course_list.html', context)



@login_required
def course_detail(request, course_id):
    """
    Display detailed information about a specific course, including materials and students.
    """
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(
        student=request.user, course=course, is_blocked=False, is_removed=False
    ).exists()
    is_teacher = request.user == course.teacher
    materials = course.materials.all()

    active_students = blocked_students = removed_students = None
    if is_teacher:
        active_students = Enrollment.objects.filter(course=course, is_blocked=False, is_removed=False)
        blocked_students = Enrollment.objects.filter(course=course, is_blocked=True)
        removed_students = Enrollment.objects.filter(course=course, is_removed=True)

    if not is_enrolled and not is_teacher:
        messages.error(request, "You do not have access to this course.")
        return redirect('courses:course_list')

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'is_teacher': is_teacher,
        'materials': materials,
        'active_students': active_students,
        'blocked_students': blocked_students,
        'removed_students': removed_students,
    })


@login_required
def course_create(request):
    """
    Allows a teacher to create a new course and add materials.
    """
    if not request.user.is_teacher:
        raise PermissionDenied("You are not authorized to create courses.")

    # Inline formset for course materials
    CourseMaterialFormSet = inlineformset_factory(
        Course, CourseMaterial, form=CourseMaterialForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = CourseForm(request.POST)
        formset = CourseMaterialFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            # Save the course with the teacher information
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()

            # Save the materials associated with the course
            materials = formset.save(commit=False)
            for material in materials:
                material.course = course
                material.save()

            formset.save_m2m()

            # Show success message to teacher
            messages.success(request, "Course created successfully!")

            return redirect('courses:course_detail', course_id=course.id)
        else:
            # If there are errors, show error message
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm()
        formset = CourseMaterialFormSet()

    return render(request, 'courses/course_form.html', {
        'form': form,
        'formset': formset,
        'course': None
    })



@login_required
def enroll_in_course(request, course_id):
    """
    Allows a student to enroll in a course. Teachers cannot enroll in their own courses.
    """
    course = get_object_or_404(Course, id=course_id)

    # Prevent teachers from enrolling in their own courses
    if course.teacher == request.user:
        return redirect('courses:course_detail', course_id=course.id)

    # Enroll the student if not already enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f'You have successfully enrolled in {course.title}.')

    return redirect('courses:course_detail', course_id=course.id)


@login_required
def edit_course(request, course_id):
    """
    Allows the course teacher to edit the course details and add materials.
    Only the course teacher can perform this action.
    """
    course = get_object_or_404(Course, id=course_id)

    # Ensure only the course teacher can edit the course
    if request.user != course.teacher:
        return render(request, '403.html', status=403)

    CourseMaterialFormSet = inlineformset_factory(
        Course, CourseMaterial, form=CourseMaterialForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        formset = CourseMaterialFormSet(request.POST, request.FILES, instance=course)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Course and materials updated successfully.")
            return redirect('courses:course_detail', course_id=course.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CourseForm(instance=course)
        formset = CourseMaterialFormSet(instance=course)

    return render(request, 'courses/course_form.html', {
        'form': form,
        'formset': formset,
        'course': course,
    })


@login_required
def delete_material(request, material_id):
    """
    Allows the course teacher to delete specific course material.
    """
    material = get_object_or_404(CourseMaterial, id=material_id)
    course = material.course
    if request.user != course.teacher:
        messages.error(request, "You do not have permission to delete this material.")
        return redirect('courses:course_detail', course_id=course.id)

    material.delete()
    messages.success(request, "Material deleted successfully.")
    return redirect('courses:course_detail', course_id=course.id)


@login_required
def add_material(request, course_id):
    """
    Allows the course teacher to add new materials to the course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, "Files have been saved successfully.")
            return redirect('courses:course_detail', course_id=course.id)
        else:
            messages.error(request, "There was an error with the form. Please try again.")
    else:
        form = CourseMaterialForm()

    return render(request, 'courses/add_material.html', {'form': form, 'course': course})


@login_required
@user_passes_test(lambda u: u.is_teacher)
def search_users(request, course_id):
    """
    Allows a teacher to search for users in a specific course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    query = request.GET.get('q', '')
    users = []
    user_info = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id)

        for user in users:
            is_actively_enrolled = Enrollment.objects.filter(
                student=user,
                course=course,
                is_removed=False,
                is_blocked=False
            ).exists()
            user_info.append({
                'user': user,
                'is_enrolled_in_teacher_course': is_actively_enrolled
            })

    return render(request, 'courses/search_results.html', {
        'user_info': user_info,
        'query': query,
        'course': course,
    })


@login_required
@user_passes_test(lambda u: u.is_teacher)
def enroll_user_in_course(request, user_id):
    """
    Allows a teacher to enroll a specific student in one of their courses.
    """
    student = get_object_or_404(User, id=user_id, is_teacher=False)
    courses = Course.objects.filter(teacher=request.user)
    selected_course_id = request.GET.get('course_id')

    if not selected_course_id:
        messages.error(request, "No course selected for enrollment.")
        return redirect('courses:course_list')

    selected_course = get_object_or_404(Course, id=selected_course_id, teacher=request.user)

    enrollment, created = Enrollment.objects.get_or_create(
        student=student,
        course=selected_course,
        defaults={'is_removed': False, 'is_blocked': False}
    )

    if not created:
        if enrollment.is_removed:
            enrollment.is_removed = False
            enrollment.save()
            messages.success(request, f"{student.username} has been re-enrolled in {selected_course.title}.")
            student_enrolled.send(sender=enrollment.__class__, student=student, course=selected_course)
        elif enrollment.is_blocked:
            messages.info(request, f"{student.username} is blocked from {selected_course.title}. Unblock the student before re-enrolling.")
        else:
            messages.info(request, f"{student.username} is already enrolled in {selected_course.title}.")
    else:
        messages.success(request, f"{student.username} has been enrolled in {selected_course.title}.")
        student_enrolled.send(sender=enrollment.__class__, student=student, course=selected_course)

    return redirect('courses:search_users', course_id=selected_course.id)


@login_required
@user_passes_test(lambda u: u.is_teacher)
def remove_student(request, course_id, student_id):
    """
    Allows the course teacher to remove a student from the course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, course=course, student__id=student_id)

    if request.method == 'POST':
        enrollment.is_removed = True
        enrollment.save()
        student_unenrolled.send(sender=enrollment.__class__, student=enrollment.student, course=course)
        messages.success(request, f"Student {enrollment.student.username} has been removed from the course.")
        return redirect('courses:course_detail', course_id=course.id)

    return render(request, 'courses/remove_student_confirm.html', {
        'course': course,
        'student': enrollment.student,
    })


@login_required
@user_passes_test(lambda u: u.is_teacher)
def block_student(request, course_id, student_id):
    """
    Allows the course teacher to block a student from accessing the course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, course=course, student__id=student_id)

    if request.method == 'POST':
        enrollment.is_blocked = True
        enrollment.save()
        student_blocked.send(sender=enrollment.__class__, student=enrollment.student, course=course)
        messages.success(request, f"Student {enrollment.student.username} has been blocked from the course.")
        return redirect('courses:course_detail', course_id=course.id)

    return render(request, 'courses/block_student_confirm.html', {
        'course': course,
        'student': enrollment.student,
    })


@login_required
@user_passes_test(lambda u: u.is_teacher)
def unblock_student(request, course_id, student_id):
    """
    Allows the course teacher to unblock a previously blocked student.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, course=course, student__id=student_id)

    if request.method == 'POST':
        enrollment.is_blocked = False
        enrollment.save()
        student_unblocked.send(sender=enrollment.__class__, student=enrollment.student, course=course)
        messages.success(request, f"Student {enrollment.student.username} has been unblocked from the course.")
        return redirect('courses:course_detail', course_id=course.id)

    return render(request, 'courses/unblock_student_confirm.html', {
        'course': course,
        'student': enrollment.student,
    })


@login_required
def delete_course(request, course_id):
    """
    Allows a teacher to delete a course they created.
    If a non-teacher tries to access this, raise PermissionDenied (403 Forbidden).
    """
    course = get_object_or_404(Course, id=course_id)

    # Ensure only the teacher can delete the course
    if request.user != course.teacher:
        raise PermissionDenied  # Raise 403 Forbidden if non-teacher attempts to delete

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course has been deleted successfully.")
        return redirect('courses:course_list')

    return render(request, 'courses/delete_course_confirm.html', {'course': course})
