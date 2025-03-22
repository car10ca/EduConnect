from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_list(request):
    """
    View to list all notifications for the logged-in user.
    Notifications are ordered by creation date, with the newest first.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """
    View to mark a specific notification as read.
    Only the owner of the notification can perform this action.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notifications_list')

@login_required
def mark_as_unread(request, notification_id):
    """
    View to mark a specific notification as unread.
    Only the owner of the notification can perform this action.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = False
    notification.save()
    return redirect('notifications:notifications_list')

@login_required
def delete_notification(request, notification_id):
    """
    View to delete a specific notification.
    Only the owner of the notification can perform this action.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return redirect('notifications:notifications_list')
