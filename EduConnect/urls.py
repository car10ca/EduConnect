from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import dashboard  # Import the dashboard view to set as the home page

urlpatterns = [
    path('admin/', admin.site.urls),  # URL pattern for the admin site
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # URL patterns for the accounts app
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),  # URL patterns for the dashboard app
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),  # URL patterns for the courses app
    path('feedback/', include(('feedback.urls', 'feedback'), namespace='feedback')),  # URL patterns for the feedback app
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),  # URL patterns for the chat app
    path('notifications/', include('notifications.urls')),  # URL patterns for the notifications app
    path('', dashboard, name='home'),  # Dashboard is also the current home page
]

# Serving media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
