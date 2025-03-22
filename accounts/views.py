from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserRegisterForm, EditProfileForm
from dashboard.forms import StatusUpdateForm
from dashboard.models import StatusUpdate

# Get the user model used in the project (custom or default)
User = get_user_model()


def register(request):
    """
    Handle user registration. If the form is valid, create a new user,
    log them in, and assign them to the appropriate group (Teachers or Students).
    """
    if request.method == 'POST':
        # Create a form instance with POST data and any uploaded files
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():  # Check if the form data is valid
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in

            # Automatically add the user to the correct group
            if user.is_teacher:
                group, created = Group.objects.get_or_create(name='Teachers')
            else:
                group, created = Group.objects.get_or_create(name='Students')
            
            user.groups.add(group)  # Add the user to the appropriate group

            return redirect('dashboard:dashboard')  # Redirect to the dashboard after registration
    else:
        form = UserRegisterForm()  # Create a blank registration form

    return render(request, 'accounts/register.html', {'form': form})  # Render the registration template


@login_required
def user_profile(request, user_id=None):
    """
    Display the user's profile. If user_id is provided, display that user's profile.
    Allows logged-in users to post a new status update.
    """
    if user_id:
        # Get the user being viewed or raise a 404 if not found
        viewed_user = get_object_or_404(User, id=user_id)
    else:
        # If no user_id is provided, show the logged-in user's profile
        viewed_user = request.user

    if request.method == 'POST':
        # Handle the status update form submission
        form = StatusUpdateForm(request.POST)
        if form.is_valid():  # Check if the form data is valid
            status_update = form.save(commit=False)  # Create a status update instance without saving to the database
            status_update.user = request.user  # Assign the status update to the logged-in user
            status_update.save()  # Save the status update
            messages.success(request, "Your status update has been posted.")  # Display a success message
            return redirect('accounts:user_profile_with_id', user_id=viewed_user.id)
    else:
        form = StatusUpdateForm()  # Create a blank status update form

    # Get the status updates of the viewed user, ordered by the latest timestamp
    status_updates = viewed_user.status_updates.order_by('-timestamp')

    return render(request, 'accounts/user_profile.html', {
        'viewed_user': viewed_user,  # Pass the viewed user's profile to the template
        'form': form,  # Pass the form to the template
        'status_updates': status_updates,  # Pass the status updates to the template
    })


@login_required
def edit_profile(request):
    """
    Allow logged-in users to edit their profile information.
    """
    if request.method == 'POST':
        # Create a form instance with POST data, uploaded files, and the current user instance
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():  # Check if the form data is valid
            form.save()  # Save the updated user data
            return redirect('accounts:user_profile')  # Redirect to the user's profile
    else:
        form = EditProfileForm(instance=request.user)  # Create a form instance with the current user data
    
    return render(request, 'accounts/edit_profile.html', {'form': form})  # Render the profile edit template
