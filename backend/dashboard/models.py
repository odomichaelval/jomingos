from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()


class DashboardPreference(models.Model):
    """User dashboard customization preferences"""
    WIDGET_CHOICES = [
        ('stats', 'Key Statistics'),
        ('charts', 'Analytics Charts'),
        ('weather', 'Weather Information'),
        ('shift_status', 'Shift Status'),
        ('quick_actions', 'Quick Actions'),
        ('kpi_cards', 'Performance Metrics'),
        ('notifications', 'Notifications'),
        ('patient_cards', 'Patient Summary'),
        ('high_risk', 'High Risk Alerts'),
        ('medium_risk', 'Medium Risk Alerts'),
        ('fall_risk', 'Fall Risk Alerts'),
        ('activity_feed', 'Activity Feed'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_preference')
    visible_widgets = models.JSONField(
        default=list,
        help_text="List of visible widget names in order"
    )
    widget_order = models.JSONField(
        default=dict,
        help_text="Widget display order"
    )
    dark_mode = models.BooleanField(default=False)
    show_notifications = models.BooleanField(default=True)
    refresh_interval = models.IntegerField(default=30, help_text="Auto-refresh interval in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Dashboard Preferences'

    def __str__(self):
        return f"{self.user.username} Dashboard Preference"

    def get_visible_widgets(self):
        if not self.visible_widgets:
            return [code for code, label in self.WIDGET_CHOICES]
        return self.visible_widgets

    def set_visible_widgets(self, widgets):
        self.visible_widgets = widgets
        self.save()


class DashboardNotification(models.Model):
    """Real-time notifications for dashboard"""
    TYPE_CHOICES = [
        ('alert', 'Alert'),
        ('warning', 'Warning'),
        ('info', 'Information'),
        ('success', 'Success'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    icon = models.CharField(max_length=50, default='bi-bell')
    action_url = models.URLField(blank=True, null=True)
    action_label = models.CharField(max_length=100, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @classmethod
    def create_notification(cls, user, notification_type, title, message, icon='bi-bell',
                          action_url=None, action_label=None, expires_in_minutes=None):
        """Helper method to create notifications"""
        expires_at = None
        if expires_in_minutes:
            expires_at = timezone.now() + timezone.timedelta(minutes=expires_in_minutes)

        return cls.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            icon=icon,
            action_url=action_url,
            action_label=action_label,
            expires_at=expires_at
        )


class DashboardActivity(models.Model):
    """Track activities for activity feed"""
    ACTIVITY_TYPES = [
        ('patient_created', 'Patient Created'),
        ('patient_updated', 'Patient Updated'),
        ('care_note_added', 'Care Note Added'),
        ('medication_administered', 'Medication Administered'),
        ('vitals_recorded', 'Vitals Recorded'),
        ('user_login', 'User Login'),
        ('report_generated', 'Report Generated'),
        ('handover_completed', 'Handover Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dashboard_activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    related_model = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.created_at}"


class UserShift(models.Model):
    """Track individual user shift times"""
    SHIFT_TYPES = [
        ('day', 'Day Shift (7am - 7pm)'),
        ('night', 'Night Shift (7pm - 7am)'),
        ('custom', 'Custom Hours'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='active_shift')
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES, default='day')
    start_time = models.TimeField(default='07:00', help_text="Shift start time (HH:MM)")
    end_time = models.TimeField(default='19:00', help_text="Shift end time (HH:MM)")
    shift_date = models.DateField(auto_now=True, help_text="Date of the shift")
    is_active = models.BooleanField(default=True, help_text="Is this shift currently active?")
    notes = models.TextField(blank=True, help_text="Any notes about the shift")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'User Shifts'
        unique_together = ['user', 'shift_date']
        ordering = ['-shift_date']
        indexes = [
            models.Index(fields=['user', '-shift_date']),
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.shift_type} ({self.shift_date})"

    @property
    def shift_end_datetime(self):
        """Get shift end as datetime for comparison"""
        from datetime import datetime, time
        from django.utils import timezone

        dt = datetime.combine(self.shift_date, self.end_time)
        # Make timezone-aware
        return timezone.make_aware(dt, timezone.get_current_timezone())

    @property
    def shift_start_datetime(self):
        """Get shift start as datetime for comparison"""
        from datetime import datetime
        from django.utils import timezone

        dt = datetime.combine(self.shift_date, self.start_time)
        # Make timezone-aware
        return timezone.make_aware(dt, timezone.get_current_timezone())

    @property
    def time_remaining_minutes(self):
        """Calculate minutes remaining in shift"""
        from django.utils import timezone

        now = timezone.now()
        if now > self.shift_end_datetime:
            return 0

        delta = self.shift_end_datetime - now
        return int(delta.total_seconds() / 60)

    @property
    def time_remaining_formatted(self):
        """Format time remaining as HH:MM"""
        minutes = self.time_remaining_minutes
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    @property
    def shift_progress_percent(self):
        """Calculate shift progress as percentage"""
        from django.utils import timezone

        now = timezone.now()
        start = self.shift_start_datetime
        end = self.shift_end_datetime

        if now >= end:
            return 100
        if now <= start:
            return 0

        total_duration = (end - start).total_seconds()
        elapsed = (now - start).total_seconds()

        return int((elapsed / total_duration) * 100) if total_duration > 0 else 0
