from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """
    Form for submitting feedback on a course.
    This form uses the Feedback model and includes fields for rating and comment.
    """
    
    class Meta:
        model = Feedback  # Specify the model to use for this form
        fields = ['rating', 'comment']  # Include only the rating and comment fields in the form
