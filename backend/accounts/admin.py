from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordResetToken, AuditLog

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


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'description', 'status', 'ip_address']
    list_filter = ['action', 'status', 'timestamp']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['timestamp', 'user', 'action', 'description', 'model_name', 'object_id', 'ip_address', 'user_agent', 'status']
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
