from django import forms
from .models import StatusUpdate


class StatusUpdateForm(forms.ModelForm):
    """
    Form for creating or updating a status update.
    Includes a single field for the content of the status update.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}),  # Textarea widget with specific size
        max_length=250,  # Maximum length for the content
        help_text='Write your status update (max 250 characters).'  # Help text displayed under the form field
    )

    class Meta:
        """
        Meta options for StatusUpdateForm.
        Specifies the model and fields to include in the form.
        """
        model = StatusUpdate  # Model associated with this form
        fields = ['content']  # Fields to be used in the form
