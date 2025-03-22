import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from feedback.models import Feedback
from notifications.models import Notification
from dashboard.models import StatusUpdate

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data for users, courses, feedback, and notifications.'

    def handle(self, *args, **kwargs):
        self._create_users()
        self._create_enrollments()
        self._create_feedback()
        self._create_status_updates()
        self._create_notifications()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _create_users(self):
        # Create additional teacher users
        User.objects.create_user(username='teacher3', email='teacher3@example.com', password='pass123', is_teacher=True)
        User.objects.create_user(username='teacher4', email='teacher4@example.com', password='pass123', is_teacher=True)
        User.objects.create_user(username='teacher5', email='teacher5@example.com', password='pass123', is_teacher=True)

        # Create additional student users
        for i in range(3, 11):
            User.objects.create_user(username=f'student{i}', email=f'student{i}@example.com', password='pass123', is_teacher=False)
        
        self.stdout.write(self.style.SUCCESS('Additional users created.'))

    def _create_enrollments(self):
        students = User.objects.filter(is_teacher=False)
        courses = Course.objects.all()
        
        # Enroll each student in 3-4 random courses
        for student in students:
            enrolled_courses = random.sample(list(courses), random.randint(3, 4))
            for course in enrolled_courses:
                Enrollment.objects.get_or_create(student=student, course=course)
        
        self.stdout.write(self.style.SUCCESS('Enrollments created.'))

    def _create_feedback(self):
        enrollments = Enrollment.objects.all()
        feedback_comments = [
            'Great course!', 'Very informative!', 'Challenging but rewarding.', 'Loved the content!',
            'Well structured course.', 'Highly recommend this to my peers.', 'Learned a lot!',
            'Clear explanations and helpful resources.', 'Course met my expectations.', 'Excellent material!'
        ]
        
        # Create 1-2 feedback entries per enrollment
        for enrollment in enrollments:
            feedback_count = random.randint(1, 2)
            for _ in range(feedback_count):
                Feedback.objects.create(
                    course=enrollment.course,
                    student=enrollment.student,
                    rating=random.randint(3, 5),  # Ratings between 3 and 5
                    comment=random.choice(feedback_comments)
                )
        
        self.stdout.write(self.style.SUCCESS('Feedback entries created.'))

    def _create_status_updates(self):
        students = User.objects.filter(is_teacher=False)
        status_messages = [
            'Excited about this course!', 'Struggling a bit with the assignments.', 'Can’t wait for the next lecture.',
            'Enjoying the learning process.', 'Got a good score on my last quiz!', 'This topic is really interesting.',
            'Trying to catch up on readings.', 'Need help with the homework.', 'Feeling confident about the final exam.',
            'Collaborating with classmates is fun!'
        ]
        
        # Create 2-3 status updates per student
        for student in students:
            update_count = random.randint(2, 3)
            for _ in range(update_count):
                StatusUpdate.objects.create(
                    user=student,
                    content=random.choice(status_messages)
                )
        
        self.stdout.write(self.style.SUCCESS('Status updates created.'))

    def _create_notifications(self):
        students = User.objects.filter(is_teacher=False)
        courses = Course.objects.all()
        
        # Notify students about their enrollments
        for student in students:
            enrolled_courses = Enrollment.objects.filter(student=student)
            for enrollment in enrolled_courses:
                Notification.objects.create(
                    user=student,
                    message=f'You have been enrolled in the course: {enrollment.course.title}.'
                )

        # Notify teachers about new feedback on their courses
        feedback_entries = Feedback.objects.all()
        for feedback in feedback_entries:
            teacher = feedback.course.teacher
            Notification.objects.create(
                user=teacher,
                message=f'New feedback from {feedback.student.username} on your course: {feedback.course.title}.'
            )

        self.stdout.write(self.style.SUCCESS('Notifications created.'))
