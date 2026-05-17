from django.db import models
from django.utils import timezone
from accounts.models import User
from patients.models import Patient


class CareNote(models.Model):

    CATEGORY_CHOICES = [
        ('observation_60',  '60 Min (Hourly) Observation'),
        ('observation_30',  '30 Min Observation'),
        ('observation_15',  '15 Min Observation'),
        ('observation_eod', 'End of Shift / Timeline Review'),
        ('personal_care',   'Personal Care'),
        ('oral_care',       'Oral Care / Dental Hygiene'),
        ('continence',      'Continence Care'),
        ('pressure_care',   'Pressure Area Care'),
        ('repositioning',   'Repositioning / Turning'),
        ('nutrition',       'Nutrition & Meal Record'),
        ('hydration',       'Fluid / Hydration Record'),
        ('weight',          'Weight Check'),
        ('mobility',        'Mobility & Moving'),
        ('activity',        'Activity & Engagement'),
        ('physiotherapy',   'Physiotherapy / Exercise'),
        ('emotional',       'Emotional Wellbeing'),
        ('behaviour',       'Behaviour / Incident Note'),
        ('sleep',           'Sleep Record'),
        ('social',          'Social Interaction'),
        ('clinical',        'Clinical / Nursing Note'),
        ('wound',           'Wound Care'),
        ('catheter',        'Catheter Care'),
        ('stoma',           'Stoma Care'),
        ('medication_note', 'Medication Note (Non-Admin)'),
        ('family_contact',  'Family / Next of Kin Contact'),
        ('gp_contact',      'GP / Healthcare Professional Contact'),
        ('safeguarding',    'Safeguarding Note'),
        ('handover',        'Shift Handover Note'),
        ('general',         'General Note'),
    ]

    PRIORITY_CHOICES = [
        ('routine',  'Routine'),
        ('important','Important'),
        ('urgent',   'Urgent'),
    ]

    LOCATION_CHOICES = [
        ('bedroom',       'Bedroom'),
        ('bathroom',      'Bathroom / Toilet'),
        ('lounge',        'Lounge / Sitting Room'),
        ('dining_room',   'Dining Room'),
        ('corridor',      'Corridor'),
        ('garden',        'Garden / Outdoor Area'),
        ('activity_room', 'Activity Room'),
        ('other',         'Other'),
    ]

    OBS_STATUS_CHOICES = [
        ('sleeping',         'Appears to be sleeping'),
        ('awake_settled',    'Awake and settled'),
        ('awake_active',     'Awake and active'),
        ('awake_distressed', 'Awake and distressed'),
        ('awake_confused',   'Awake and confused'),
        ('engaged',          'Engaged in activity'),
        ('eating',           'Eating / drinking'),
        ('personal_care',    'Receiving personal care'),
        ('other',            'Other — see notes'),
    ]

    WASH_CHOICES = [
        ('full_bed_bath',   'Full bed bath'),
        ('assisted_shower', 'Assisted shower'),
        ('assisted_bath',   'Assisted bath'),
        ('stand_wash',      'Stand-up wash'),
        ('face_hands',      'Face and hands only'),
        ('declined',        'Resident declined'),
    ]

    ORAL_CARE_CHOICES = [
        ('teeth_brushed',    'Teeth brushed'),
        ('dentures_cleaned', 'Dentures cleaned'),
        ('mouthwash',        'Mouthwash used'),
        ('declined',         'Resident declined'),
    ]

    CONTINENCE_CHOICES = [
        ('continent',          'Continent'),
        ('pad_changed',        'Pad / incontinence aid changed'),
        ('catheter_emptied',   'Catheter bag emptied'),
        ('toileted',           'Assisted to toilet'),
        ('incontinent_urine',  'Incontinent of urine'),
        ('incontinent_faeces', 'Incontinent of faeces'),
        ('incontinent_both',   'Incontinent of urine and faeces'),
        ('constipated',        'Reported constipation'),
        ('diarrhoea',          'Diarrhoea noted'),
    ]

    PRESSURE_AREA_CHOICES = [
        ('intact',          'Skin intact — no concerns'),
        ('redness',         'Redness / discolouration noted'),
        ('blister',         'Blister noted'),
        ('wound_present',   'Wound present — see wound care note'),
        ('heels_offloaded', 'Heels offloaded'),
        ('cream_applied',   'Barrier / moisturising cream applied'),
    ]

    MEAL_CHOICES = [
        ('breakfast',         'Breakfast'),
        ('mid_morning_snack', 'Mid-morning snack'),
        ('lunch',             'Lunch'),
        ('afternoon_tea',     'Afternoon tea'),
        ('dinner',            'Dinner'),
        ('evening_snack',     'Evening snack'),
        ('supplement',        'Nutritional supplement'),
    ]

    APPETITE_CHOICES = [
        ('all',     'All eaten'),
        ('most',    'Most eaten (75%+)'),
        ('half',    'About half eaten (50%)'),
        ('little',  'Little eaten (25%)'),
        ('none',    'Nothing eaten'),
        ('declined','Meal declined'),
        ('fed',     'Required feeding assistance'),
        ('peg',     'PEG / enteral feed'),
    ]

    FLUID_INTAKE_CHOICES = [
        ('good',      'Good (1500ml+)'),
        ('adequate',  'Adequate (1000–1499ml)'),
        ('poor',      'Poor (<1000ml)'),
        ('declined',  'Fluids declined'),
        ('thickened', 'Thickened fluids only'),
        ('iv_fluids', 'IV fluids in progress'),
    ]

    MOOD_CHOICES = [
        ('happy',                'Happy / content'),
        ('settled',              'Calm and settled'),
        ('anxious',              'Anxious / worried'),
        ('low',                  'Low mood / tearful'),
        ('agitated',             'Agitated / restless'),
        ('aggressive',           'Verbally aggressive'),
        ('physically_aggressive','Physically aggressive'),
        ('confused',             'Confused / disoriented'),
        ('withdrawn',            'Withdrawn / uncommunicative'),
        ('fatigued',             'Tired / fatigued'),
    ]

    SLEEP_QUALITY_CHOICES = [
        ('good', 'Good — slept through'),
        ('fair', 'Fair — some waking'),
        ('poor', 'Poor — frequently awake'),
        ('none', 'Did not sleep'),
        ('nap',  'Short nap only'),
    ]

    MOBILITY_AID_CHOICES = [
        ('independent',  'Independent — no aid'),
        ('walking_stick','Walking stick'),
        ('zimmer_frame', 'Zimmer frame / walking frame'),
        ('rollator',     'Rollator / wheeled walker'),
        ('wheelchair',   'Wheelchair'),
        ('hoist',        'Hoist required'),
        ('two_staff',    'Two staff assist'),
        ('one_staff',    'One staff assist'),
        ('bed_bound',    'Bed-bound'),
    ]

    # Core
    patient   = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='care_notes')
    author    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='care_notes')
    category  = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    priority  = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='routine')
    note_text = models.TextField(blank=True)
    created_at= models.DateTimeField(default=timezone.now)

    # Observation
    obs_location  = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True)
    obs_status    = models.CharField(max_length=30, choices=OBS_STATUS_CHOICES, blank=True)
    obs_completed = models.BooleanField(default=False)

    # Personal care
    wash_type             = models.CharField(max_length=20, choices=WASH_CHOICES, blank=True)
    oral_care             = models.CharField(max_length=20, choices=ORAL_CARE_CHOICES, blank=True)
    continence            = models.CharField(max_length=25, choices=CONTINENCE_CHOICES, blank=True)
    pressure_area         = models.CharField(max_length=20, choices=PRESSURE_AREA_CHOICES, blank=True)
    repositioned          = models.BooleanField(default=False)
    repositioned_position = models.CharField(max_length=50, blank=True)

    # Nutrition
    meal_time      = models.CharField(max_length=25, choices=MEAL_CHOICES, blank=True)
    appetite       = models.CharField(max_length=10, choices=APPETITE_CHOICES, blank=True)
    fluid_intake   = models.CharField(max_length=10, choices=FLUID_INTAKE_CHOICES, blank=True)
    fluid_amount_ml= models.PositiveIntegerField(null=True, blank=True)
    weight_kg      = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)

    # Wellbeing
    mood          = models.CharField(max_length=30, choices=MOOD_CHOICES, blank=True)
    sleep_quality = models.CharField(max_length=10, choices=SLEEP_QUALITY_CHOICES, blank=True)
    sleep_hours   = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    # Mobility
    mobility_aid        = models.CharField(max_length=20, choices=MOBILITY_AID_CHOICES, blank=True)
    falls_risk_observed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_category_display()} note for {self.patient} by {self.author}'

    @property
    def priority_color(self):
        return {'routine': 'success', 'important': 'warning', 'urgent': 'danger'}.get(self.priority, 'secondary')

    @property
    def category_icon(self):
        icons = {
            'observation_60': 'bi-clock',
            'observation_30': 'bi-clock-history',
            'observation_15': 'bi-alarm',
            'observation_eod':'bi-clipboard-check',
            'personal_care':  'bi-droplet',
            'oral_care':      'bi-emoji-smile',
            'continence':     'bi-droplet-half',
            'pressure_care':  'bi-bandaid',
            'repositioning':  'bi-arrow-repeat',
            'nutrition':      'bi-cup-hot',
            'hydration':      'bi-cup-straw',
            'weight':         'bi-graph-up',
            'mobility':       'bi-person-walking',
            'activity':       'bi-controller',
            'physiotherapy':  'bi-heart-pulse',
            'emotional':      'bi-emoji-heart-eyes',
            'behaviour':      'bi-exclamation-triangle',
            'sleep':          'bi-moon-stars',
            'social':         'bi-people',
            'clinical':       'bi-clipboard2-pulse',
            'wound':          'bi-bandaid-fill',
            'catheter':       'bi-droplet-fill',
            'stoma':          'bi-circle',
            'medication_note':'bi-capsule',
            'family_contact': 'bi-telephone',
            'gp_contact':     'bi-hospital',
            'safeguarding':   'bi-shield-exclamation',
            'handover':       'bi-arrow-left-right',
            'general':        'bi-journal-text',
        }
        return icons.get(self.category, 'bi-journal')
