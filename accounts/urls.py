from django.urls import path, reverse_lazy
from .views import register, user_profile, edit_profile
from django.contrib.auth import views as auth_views

# Define the namespace for the accounts app
app_name = 'accounts'

urlpatterns = [
    # Registration view
    path('register/', register, name='register'),

    # Login view
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),

    # Logout view; redirects to login after logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page=reverse_lazy('accounts:login')),
        name='logout'
    ),

    # User profile view
    path('profile/', user_profile, name='user_profile'),

    # User profile with ID - using the user_profile view directly
    path('profile/<int:user_id>/', user_profile, name='user_profile_with_id'),

    # Edit profile view
    path('profile/edit/', edit_profile, name='edit_profile'),

    # Password change view; displays the form for changing passwords
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url=reverse_lazy('accounts:password_change_done')
        ),
        name='password_change'
    ),

    # Password change done view; shows a confirmation page after a successful password change
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # Password reset view; displays the form for requesting a password reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'
    ),

    # Password reset done view; displays a confirmation message after the reset email is sent
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Password reset confirm view; allows the user to reset their password via a unique link
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),

    # Password reset complete view; shows a confirmation message after a successful password reset
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
