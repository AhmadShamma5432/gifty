from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Customizing the UserAdmin for the custom User model
class CustomUserAdmin(UserAdmin):
    # Customize the admin site header and title
    admin.site.site_header = "Gifty Admin Panel"
    admin.site.site_title = "Gifty Admin Portal"
    admin.site.index_title = "Welcome to Gifty's Admin Panel"

    # Fields to display in the list view
    list_display = ('email', 'name', 'phone_number', 'is_active', 'is_staff', 'is_superuser')

    # Fields to filter by in the right sidebar
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Fields to search in the search bar
    search_fields = ('email', 'name', 'phone_number')

    # Fields to edit directly from the list view
    list_editable = ('is_active',)

    # Fieldsets for organizing fields in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )

    # Add fieldsets for creating a new user in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    # Make the email field read-only after creation
    readonly_fields = ('last_login',)

    # Ordering of users in the list view
    ordering = ('email',)

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)