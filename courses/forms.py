from django import forms
from .models import Course, CourseMaterial


class CourseForm(forms.ModelForm):
    """
    Form for creating or updating a Course.
    Includes fields for the course title and description.
    """
    title = forms.CharField(required=True, max_length=200)  # Title of the course, required field
    description = forms.CharField(required=True, widget=forms.Textarea)  # Description of the course, required field

    class Meta:
        """
        Meta options for CourseForm.
        Specifies the model and fields to include in the form.
        """
        model = Course
        fields = ['title', 'description']  # Fields to be used in the form


class CourseMaterialForm(forms.ModelForm):
    """
    Form for adding or updating course materials.
    Includes a file field with specific file type acceptance.
    """
    class Meta:
        """
        Meta options for CourseMaterialForm.
        Specifies the model and fields to include in the form.
        """
        model = CourseMaterial
        fields = ['file']  # Field to be used in the form
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.txt,.doc,.docx,.png,.jpg,.jpeg'})
        }  # Widget settings to restrict file types
