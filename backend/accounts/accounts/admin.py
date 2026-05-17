from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetToken

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'role', 'email', 'is_active', 'is_on_duty']
    list_filter = ['role', 'is_active', 'is_on_duty']
    fieldsets = UserAdmin.fieldsets + (
        ('Jomingos', {'fields': ('role', 'phone_number', 'job_title', 'is_on_duty', 'profile_image')}),
    )

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'expires_at', 'is_used', 'created_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    readonly_fields = ['token', 'token_plain', 'created_at']
    search_fields = ['user__username', 'user__email']
