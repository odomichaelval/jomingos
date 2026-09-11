from django.db import models
from django.utils import timezone
from accounts.models import User


class Patient(models.Model):
    CARE_LEVEL_CHOICES = [
        ('residential', 'Residential'),
        ('nursing', 'Nursing Care'),
        ('dementia', 'Dementia Care'),
        ('respite', 'Respite Care'),
        ('palliative', 'Palliative Care'),
    ]
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    nhs_number = models.CharField(max_length=20, blank=True, unique=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)

    # Admission
    room_number = models.CharField(max_length=10, blank=True)
    admission_date = models.DateField(default=timezone.now)
    care_level = models.CharField(max_length=20, choices=CARE_LEVEL_CHOICES, default='residential')
    primary_nurse = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='primary_patients', limit_choices_to={'role': 'nurse'}
    )

    # Medical
    allergies = models.TextField(blank=True, help_text='List known allergies')
    medical_conditions = models.TextField(blank=True)
    dietary_requirements = models.TextField(blank=True)
    mobility_status = models.CharField(max_length=100, blank=True)

    # Emergency
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    gp_name = models.CharField(max_length=100, blank=True)
    gp_phone = models.CharField(max_length=20, blank=True)

    # System
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='patients/', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_age(self):
        from datetime import date
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def get_fall_risk(self):
        score = 0
        reasons = []

        # Factor 1 — Age
        age = self.get_age()
        if age >= 90:
            score += 20
            reasons.append(f'Age {age} (very high risk age group)')
        elif age >= 80:
            score += 15
            reasons.append(f'Age {age} (high risk age group)')
        elif age >= 70:
            score += 8
            reasons.append(f'Age {age} (moderate risk age group)')

        # Factor 2 — NEWS2 Score from latest vitals
        try:
            from vitals.models import VitalSigns
            latest_v = VitalSigns.objects.filter(patient=self).order_by('-recorded_at').first()
            if latest_v:
                news2 = latest_v.news2_total
                if news2 >= 7:
                    score += 25
                    reasons.append(f'NEWS2 score {news2} — HIGH RISK (immediate deterioration)')
                elif news2 >= 5:
                    score += 15
                    reasons.append(f'NEWS2 score {news2} — Medium risk')
                elif news2 >= 3:
                    score += 8
                    reasons.append(f'NEWS2 score {news2} — Low-medium risk')
        except Exception:
            pass

        # Factor 3 — Mobility Aid from latest care note
        try:
            from care_notes.models import CareNote
            latest_mobility = CareNote.objects.filter(patient=self).exclude(mobility_aid='').order_by('-created_at').first()
            if latest_mobility:
                aid = latest_mobility.mobility_aid
                aid_scores = {
                    'hoist': 25, 'two_staff': 20, 'one_staff': 15,
                    'zimmer_frame': 12, 'rollator': 10, 'walking_stick': 8,
                    'wheelchair': 8, 'bed_bound': 5, 'independent': 0,
                }
                pts = aid_scores.get(aid, 0)
                if pts > 0:
                    score += pts
                    reasons.append(f'Mobility aid: {latest_mobility.get_mobility_aid_display()}')
        except Exception:
            pass

        # Factor 4 — Mood / Confusion from latest care note
        try:
            from care_notes.models import CareNote
            latest_mood = CareNote.objects.filter(patient=self).exclude(mood='').order_by('-created_at').first()
            if latest_mood:
                mood = latest_mood.mood
                mood_scores = {
                    'confused': 20, 'agitated': 18, 'physically_aggressive': 15,
                    'anxious': 10, 'withdrawn': 8, 'low': 5,
                    'fatigued': 8, 'settled': 0, 'happy': 0,
                }
                pts = mood_scores.get(mood, 0)
                if pts > 0:
                    score += pts
                    reasons.append(f'Mood recorded: {latest_mood.get_mood_display()}')
        except Exception:
            pass

        # Factor 5 — Sleep disturbance
        try:
            from care_notes.models import CareNote
            last_24h = timezone.now() - timezone.timedelta(hours=24)
            latest_sleep = CareNote.objects.filter(patient=self, created_at__gte=last_24h).exclude(sleep_quality='').order_by('-created_at').first()
            if latest_sleep:
                sleep_scores = {
                    'none': 18, 'poor': 12, 'fair': 6, 'nap': 8, 'good': 0,
                }
                pts = sleep_scores.get(latest_sleep.sleep_quality, 0)
                if pts > 0:
                    score += pts
                    reasons.append(f'Sleep quality: {latest_sleep.get_sleep_quality_display()}')
        except Exception:
            pass

        # Factor 6 — Care level
        care_level_scores = {
            'dementia': 20, 'nursing': 10, 'palliative': 8,
            'respite': 5, 'residential': 0,
        }
        pts = care_level_scores.get(self.care_level, 0)
        if pts > 0:
            score += pts
            reasons.append(f'Care level: {self.get_care_level_display()}')

        # Factor 7 — Time of day multiplier
        current_hour = timezone.localtime(timezone.now()).hour
        is_night = current_hour >= 19 or current_hour < 7
        if is_night:
            score = int(score * 1.3)
            reasons.append('Night shift multiplier applied (19:00–07:00)')

        # Cap at 100
        score = min(score, 100)

        if score >= 70:
            level, color, label = 'high', 'danger', 'HIGH RISK'
        elif score >= 40:
            level, color, label = 'medium', 'warning', 'MEDIUM RISK'
        else:
            level, color, label = 'low', 'success', 'LOW RISK'

        return {
            'score': score,
            'level': level,
            'color': color,
            'label': label,
            'reasons': reasons,
        }

    @property
    def care_level_badge(self):
        colors = {
            'residential': 'success',
            'nursing': 'primary',
            'dementia': 'warning',
            'respite': 'info',
            'palliative': 'danger',
        }
        return colors.get(self.care_level, 'secondary')

    @property
    def initials(self):
        return f'{self.first_name[0]}{self.last_name[0]}'.upper()

    @property
    def has_allergies(self):
        return bool(self.allergies.strip())