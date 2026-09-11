from django.db import models
from django.utils import timezone
from accounts.models import User
from patients.models import Patient


class Medication(models.Model):
    ROUTE_CHOICES = [
        ('oral', 'Oral'), ('iv', 'Intravenous'), ('im', 'Intramuscular'),
        ('sc', 'Subcutaneous'), ('topical', 'Topical'), ('inhaled', 'Inhaled'),
        ('sublingual', 'Sublingual'), ('rectal', 'Rectal'), ('nasal', 'Nasal'),
    ]
    MED_TYPE_CHOICES = [
        ('regular', 'Regular'), ('prn', 'PRN (As Required)'),
        ('stat', 'STAT (Immediate)'), ('tto', 'TTO (To Take Out)'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medications_given')
    drug_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    route = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    med_type = models.CharField(max_length=10, choices=MED_TYPE_CHOICES)
    administered_at = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    witnessed_by = models.CharField(max_length=100, blank=True)
    refused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-administered_at']

    def __str__(self):
        return f'{self.drug_name} {self.dosage} for {self.patient}'

    @property
    def route_icon(self):
        icons = {'oral': 'bi-capsule', 'iv': 'bi-droplet-fill', 'topical': 'bi-bandaid',
                 'inhaled': 'bi-wind', 'im': 'bi-syringe', 'sc': 'bi-syringe'}
        return icons.get(self.route, 'bi-capsule-pill')

    @property
    def type_badge(self):
        colors = {'regular': 'primary', 'prn': 'warning', 'stat': 'danger', 'tto': 'info'}
        return colors.get(self.med_type, 'secondary')

  #Voice recording for AI extraction

class VoiceMedicationDraft(models.Model):
    """Temporary draft created from voice recording, pending staff review."""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    audio_file = models.FileField(upload_to='voice_medications/', blank=True, null=True)
    transcript = models.TextField(blank=True)

    # AI-extracted draft values (mirrors Medication fields)
    drug_name = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    route = models.CharField(max_length=20, blank=True)     # validated against ROUTE_CHOICES before saving
    med_type = models.CharField(max_length=10, blank=True)   # validated against MED_TYPE_CHOICES before saving
    reason = models.CharField(max_length=200, blank=True)
    witnessed_by = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [('pending', 'Pending Review'), ('confirmed', 'Confirmed'), ('discarded', 'Discarded')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Voice medication draft for {self.patient} at {self.created_at}'