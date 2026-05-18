from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('care_assistant', 'Care Assistant'),
        ('family', 'Family Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='care_assistant')
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True)
    is_on_duty = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_nurse(self):
        return self.role == 'nurse'

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_care_assistant(self):
        return self.role == 'care_assistant'
    
    @property
    def is_family(self):
        return self.role == 'family'

    @property
    def role_badge_color(self):
        colors = {
            'admin': 'danger',
            'doctor': 'primary',
            'nurse': 'success',
            'care_assistant': 'warning',
        }
        return colors.get(self.role, 'secondary')

    @property
    def initials(self):
        parts = (self.get_full_name() or self.username).split()
        return ''.join(p[0].upper() for p in parts[:2])


class PasswordResetToken(models.Model):
    """Secure token for password reset flow"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True, db_index=True)  # hashed token
    token_plain = models.CharField(max_length=255, editable=False)  # temp storage for generation
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Password Reset Tokens'

    def __str__(self):
        return f'{self.user.username} - Reset Token'

    @staticmethod
    def generate_token():
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(32)

    def is_valid(self):
        """Check if token is valid (not expired and not used)"""
        return not self.is_used and timezone.now() < self.expires_at

    def mark_as_used(self):
        """Mark token as used"""
        self.is_used = True
        self.save(update_fields=['is_used'])
