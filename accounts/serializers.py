from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model, handles conversion of User objects
    into JSON format and vice-versa. This is used to fetch user data.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_photo', 'is_teacher']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. This serializer is used to handle
    user creation including password validation.
    """
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'is_teacher']

    def validate(self, data):
        """
        Check that the two password fields match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create a new user with the provided data.
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile. This includes fields that
    a user can update (e.g., first name, last name, profile photo).
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_photo']
