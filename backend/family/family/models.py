from django.db import models
from accounts.models import User
from patients.models import Patient


class FamilyMember(models.Model):
    RELATION_CHOICES = [
        ('son',         'Son'),
        ('daughter',    'Daughter'),
        ('spouse',      'Spouse / Partner'),
        ('sibling',     'Brother / Sister'),
        ('parent',      'Parent'),
        ('grandchild',  'Grandchild'),
        ('friend',      'Close Friend'),
        ('carer',       'External Carer'),
        ('other',       'Other'),
    ]

    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='family_profile')
    patient  = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='family_members')
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES, default='other')
    approved = models.BooleanField(default=True)
    notes    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name()} ({self.get_relation_display()}) — {self.patient}'