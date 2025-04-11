from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view of the admin panel
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    # Fields to display in the edit form of the admin panel
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('role',)}),  # Add your custom fields here
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to display in the add form of the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    # Add filters for the list view
    list_filter = ('role', 'is_staff', 'is_active')

    # Add search functionality
    search_fields = ('username', 'email', 'role')

# Register the User model with the custom UserAdmin
admin.site.register(User, CustomUserAdmin)