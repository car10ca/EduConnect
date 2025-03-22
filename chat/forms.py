from django import forms
from .models import ChatSession
from accounts.models import User


class CreateRoomForm(forms.ModelForm):
    """
    Form for creating a new chat room.
    Allows specifying the room name, privacy setting, and allowed users.
    """

    allowed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Queryset for selecting users
        required=False,  # Field is optional
        widget=forms.CheckboxSelectMultiple  # Use checkboxes for selection
    )

    class Meta:
        """
        Meta options for the CreateRoomForm.
        Specifies the model and fields to include in the form.
        """
        model = ChatSession
        fields = ['name', 'is_private', 'allowed_users']  # Fields to be included in the form

    def clean_name(self):
        """
        Custom validation for the 'name' field.
        Ensures that the room name is provided.
        """
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Room name is required.")
        return name
