from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'phone', 'full_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'address', 'date_of_birth', 'citizenship_no', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    search_fields = ['phone', 'full_name', 'email']
    readonly_fields = ['last_login', 'date_joined']

admin.site.register(User, UserAdmin)
