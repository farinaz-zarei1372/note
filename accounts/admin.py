from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class Customuseradmin(UserAdmin):
    list_display = ["id", "email", "is_active", "is_staff", "is_superuser"]
    search_fields = ["email"]
    ordering = ["email"]
    fieldsets = [
        ("Authentication", {"fields": ["email", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_active", "is_superuser"]}),
        ("Groups", {"fields": ["groups", "user_permissions"]}),
        ("Important date", {"fields": ["last_login"]}),
    ]

    add_fieldsets = [
        ("personal info",
         {"fields": ["email", "password1", "password2", "is_staff", "is_active", "is_superuser"]}),
    ]


admin.site.register(User, Customuseradmin)
admin.site.register(Profile)

# Register your models here.
