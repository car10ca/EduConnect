import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import ChatSession, ChatAccessAttempt
from .forms import CreateRoomForm

# Get an instance of a logger
logger = logging.getLogger('chat_access')


@login_required
def chat_home(request):
    """
    View for the chat home page.
    Handles room creation via POST requests and displays existing chat sessions.
    """
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            is_private = form.cleaned_data['is_private']
            allowed_users = form.cleaned_data['allowed_users']

            # Set expiry time for private rooms (default 10 minutes), None for public rooms
            expiry_time = timezone.now() + timedelta(minutes=10) if is_private else None

            # Create a new chat session
            chat_session = ChatSession.objects.create(
                name=room_name,
                created_by=request.user,
                is_private=is_private,
                expiry_time=expiry_time  # Set expiry_time based on privacy
            )

            # Add the creator and any allowed users as participants
            chat_session.participants.add(request.user)
            chat_session.allowed_users.add(request.user)
            chat_session.allowed_users.add(*allowed_users)
            chat_session.save()

            messages.success(request, f"Chat room '{room_name}' created successfully.")
            return redirect('chat:room', room_name=chat_session.name)
        else:
            messages.error(request, "Room name cannot be empty. Please enter a valid room name.")
    else:
        form = CreateRoomForm()

    # Display all chat sessions
    chat_sessions = ChatSession.objects.all()
    return render(request, 'chat/chat_home.html', {
        'chat_sessions': chat_sessions,
        'form': form
    })


from django.http import HttpResponseForbidden  # Import this for forbidden responses

@login_required
def room(request, room_name):
    """
    View for handling chat room access.
    Provides access control for predefined and user-created chat rooms.
    """
    # Define predefined rooms
    predefined_rooms = ['students', 'teachers', 'teacher_student']

    if room_name in predefined_rooms:
        chat_session, created = ChatSession.objects.get_or_create(
            name=room_name,
            defaults={'created_by': request.user, 'is_private': False}
        )
    else:
        chat_session = get_object_or_404(ChatSession, name=room_name)

    # Log access attempt
    access_attempt = ChatAccessAttempt(
        user=request.user,
        room_name=room_name,
        success=False  # Set to false initially, updated if access is granted
    )

    # Access control for predefined rooms
    if room_name == 'students' and not request.user.groups.filter(name='Students').exists():
        logger.info(f"Access denied to {request.user.username} for room '{room_name}'")
        access_attempt.save()
        return HttpResponseForbidden(render(request, 'chat/access_denied.html', {
            'room_name': room_name,
            'message': "You do not have permission to enter the Students Only Room."
        }))

    if room_name == 'teachers' and not request.user.groups.filter(name='Teachers').exists():
        logger.info(f"Access denied to {request.user.username} for room '{room_name}'")
        access_attempt.save()
        return HttpResponseForbidden(render(request, 'chat/access_denied.html', {
            'room_name': room_name,
            'message': "You do not have permission to enter the Teachers Only Room."
        }))

    # Access control for private rooms
    if chat_session.is_private and request.user not in chat_session.allowed_users.all():
        logger.info(f"Access denied to {request.user.username} for room '{room_name}'")
        access_attempt.save()
        return HttpResponseForbidden(render(request, 'chat/access_denied.html', {
            'room_name': room_name,
            'message': "You do not have permission to enter this private chat room."
        }))

    # Log successful access
    access_attempt.success = True
    access_attempt.save()

    # Ensure user is added as a participant
    chat_session.participants.add(request.user)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat_session': chat_session
    })

@login_required
def delete_room(request, room_name):
    """
    View to delete a chat room.
    Only the creator of the room can delete it.
    """
    chat_session = get_object_or_404(ChatSession, name=room_name)

    # Ensure that only the creator can delete the room
    if chat_session.created_by != request.user:
        logger.error(f"User {request.user.username} attempted to delete room '{room_name}' but is not the creator.")
        raise PermissionDenied("You do not have permission to delete this chat room.")

    logger.info(f"{request.user.username} deleted chat room '{room_name}'")
    chat_session.delete()
    messages.success(request, f"Chat room '{room_name}' has been deleted successfully.")
    return redirect('chat:chat_home')
