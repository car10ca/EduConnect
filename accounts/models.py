from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.
    Adds additional fields to manage user profiles and roles.
    """

    profile_photo = models.ImageField(
        upload_to='profiles/', 
        null=True, 
        blank=True
    )
    is_teacher = models.BooleanField(default=False)  # True for teachers, False for students
