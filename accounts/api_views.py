from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserProfileUpdateSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    """
    API view to handle user registration.
    Only unauthenticated users should access this endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve user details.
    This view is protected and can only be accessed by the logged-in user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override to return the currently logged-in user.
        """
        return self.request.user

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    """
    API view to handle updating the user profile.
    This view is protected and allows users to update their own profile details.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override to return the currently logged-in user.
        """
        return self.request.user
