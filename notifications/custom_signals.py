from django.dispatch import Signal

# Custom signals to handle specific events that are not directly tied to model lifecycle events.
# These signals are used to decouple the logic for handling student status changes (blocked, unblocked, unenrolled, enrolled)
# from the models and to provide a more flexible way to trigger actions in response to these events.

student_blocked = Signal()     # Signal sent when a student is blocked from a course
student_unblocked = Signal()   # Signal sent when a student is unblocked in a course
student_unenrolled = Signal()  # Signal sent when a student is unenrolled from a course
student_enrolled = Signal()    # Signal sent when a student is enrolled in a course
