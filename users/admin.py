"""User admin classes."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Models
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin."""
    list_display = ('pk', 'user', 'phone_number',
                    'website', 'picture')

    list_display_links = ('pk', 'user')
    list_editable = ('phone_number', 'website')
    list_filter = ('created', 'modified', 'user__is_active')

    search_fields = ('user__first_name', 'user__last_name',
                     'phone_number')

    fieldsets = [
        ('Profile', {'fields': ('user', 'picture'), }),
        ('Extra info', {'fields': (('website', 'phone_number'), ('biography'),)}),
        ('Metadata', {'fields': (('created', 'modified'))}),
    ]

    readonly_fields = ('created', 'modified')


class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin."""
    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
