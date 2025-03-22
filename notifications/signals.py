from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Enrollment, CourseMaterial
from feedback.models import Feedback
from notifications.models import Notification
from notifications.custom_signals import student_blocked, student_unblocked, student_unenrolled

@receiver(post_save, sender=Enrollment)
def notify_on_enrollment(sender, instance, created, **kwargs):
    """
    Sends notifications when a student enrolls in a course.
    Notifies both the student and the course teacher.
    """
    course = instance.course
    student = instance.student
    teacher = course.teacher

    if created:
        # Notify the teacher about the new student enrollment
        teacher_message = f"New student '{student.username}' enrolled in your course: {course.title}"
        Notification.objects.create(user=teacher, message=teacher_message)
        
        # Notify the student about their enrollment
        student_message = f"You have been enrolled in the course: {course.title}"
        Notification.objects.create(user=student, message=student_message)

@receiver(post_save, sender=CourseMaterial)
def notify_students_on_new_material(sender, instance, created, **kwargs):
    """
    Sends notifications to all students enrolled in a course when new material is added.
    """
    if created:
        course = instance.course
        enrollments = Enrollment.objects.filter(course=course)
        message = f"New material added to the course: {course.title}"
        for enrollment in enrollments:
            Notification.objects.create(user=enrollment.student, message=message)

@receiver(post_save, sender=Feedback)
def notify_teacher_on_feedback(sender, instance, created, **kwargs):
    """
    Sends a notification to the course teacher when new feedback is received from a student.
    """
    if created:
        course = instance.course
        teacher = course.teacher
        student = instance.student
        message = f"New feedback from '{student.username}' on your course: {course.title}"
        Notification.objects.create(user=teacher, message=message)

# Custom signal handlers for student status changes

@receiver(student_blocked)
def notify_student_on_block(sender, student, course, **kwargs):
    """
    Sends a notification to a student when they are blocked from a course.
    """
    message = f"You have been blocked from the course: {course.title}."
    Notification.objects.create(user=student, message=message)

@receiver(student_unblocked)
def notify_student_on_unblock(sender, student, course, **kwargs):
    """
    Sends a notification to a student when they are unblocked in a course.
    """
    message = f"You have been unblocked from the course: {course.title}."
    Notification.objects.create(user=student, message=message)

@receiver(student_unenrolled)
def notify_student_on_unenroll(sender, student, course, **kwargs):
    """
    Sends a notification to a student when they are unenrolled from a course.
    """
    message = f"You have been unenrolled from the course: {course.title}."
    Notification.objects.create(user=student, message=message)
