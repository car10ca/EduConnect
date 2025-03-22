from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Define a custom admin class for the User model
class UserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin to manage User model fields and behavior in the Django admin interface.
    This class customizes the user listing, filtering, and form display in the admin panel.
    """
    # Specify the fields to be displayed in the admin list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_teacher', 'is_staff'
    )
    
    # Specify the fields that can be used to filter the admin list view
    list_filter = (
        'is_teacher', 'is_staff', 'is_superuser', 'is_active', 'groups'
    )
    
    # Define fieldsets to control layout of user detail view in admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'profile_photo')
        }),
        ('Permissions', {
            'fields': (
                'is_teacher', 'is_active', 'is_staff', 
                'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Define fields to be displayed when adding a new user via the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'is_teacher', 
                'is_active', 'is_staff', 'is_superuser', 'groups', 
                'user_permissions'
            ),
        }),
    )
    
    # Specify the fields to be used for searching in the admin
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Specify the default ordering for user list view
    ordering = ('username',)
    
    # Enable horizontal filter interface for many-to-many relationships
    filter_horizontal = ('groups', 'user_permissions')


# Register the custom UserAdmin with the User model
admin.site.register(User, UserAdmin)
