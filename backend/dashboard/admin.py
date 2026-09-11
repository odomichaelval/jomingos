from django.contrib import admin
from .models import DashboardPreference, DashboardNotification, DashboardActivity, UserShift


@admin.register(DashboardPreference)
class DashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'dark_mode', 'show_notifications', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DashboardNotification)
class DashboardNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(DashboardActivity)
class DashboardActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'user', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(UserShift)
class UserShiftAdmin(admin.ModelAdmin):
    list_display = ['user', 'shift_date', 'shift_type', 'start_time', 'end_time', 'is_active']
    list_filter = ['shift_type', 'is_active', 'shift_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User & Date', {
            'fields': ('user', 'shift_date')
        }),
        ('Shift Details', {
            'fields': ('shift_type', 'start_time', 'end_time', 'is_active')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'shift_date'
