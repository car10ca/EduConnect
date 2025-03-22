from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

# Get the user model used in the project (custom or default)
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    """
    Custom form for user registration, extending Django's built-in UserCreationForm.
    This form adds additional fields for user role and profile photo.
    """

    is_teacher = forms.BooleanField(
        required=False, 
        help_text="Check if registering as a teacher."
    )
    profile_photo = forms.ImageField(required=False)

    class Meta:
        """
        Meta options for UserRegisterForm.
        Specifies the model and the fields to include in the form.
        """
        model = User
        fields = [
            'username', 'email', 'password1', 
            'password2', 'is_teacher', 'profile_photo'
        ]

    def save(self, commit=True):
        """
        Overriding the save method to handle custom behavior.
        Assigns the is_teacher attribute based on the form input.
        """
        user = super().save(commit=False)
        user.is_teacher = self.cleaned_data['is_teacher']
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    """
    Custom form for editing user profile, extending Django's UserChangeForm.
    Adds a profile photo field and excludes the password field from the form.
    """

    profile_photo = forms.ImageField(
        required=False, 
        label='Profile Photo'
    )

    class Meta:
        """
        Meta options for EditProfileForm.
        Specifies the model and the fields to include in the form.
        """
        model = User
        fields = ['username', 'email', 'profile_photo']

    def __init__(self, *args, **kwargs):
        """
        Customize the form initialization.
        Remove the password field to avoid confusion when editing the profile.
        """
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
