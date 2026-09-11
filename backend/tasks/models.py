from django.db import models
from django.utils import timezone
from accounts.models import User
from patients.models import Patient


class CareTask(models.Model):

    PRIORITY_CHOICES = [
        ('high',   'High Priority'),
        ('medium', 'Medium Priority'),
        ('low',    'Low Priority'),
    ]

    SHIFT_CHOICES = [
        ('morning',   'Morning (07:00–13:00)'),
        ('afternoon', 'Afternoon (13:00–19:00)'),
        ('night',     'Night (19:00–07:00)'),
    ]

    TASK_CHOICES = [
        # ── OBSERVATION & MONITORING ──────────────────────────────────────
        ('obs_60_07',               '60 Min Observation — 07:00'),
        ('obs_60_08',               '60 Min Observation — 08:00'),
        ('obs_60_09',               '60 Min Observation — 09:00'),
        ('obs_60_10',               '60 Min Observation — 10:00'),
        ('obs_60_11',               '60 Min Observation — 11:00'),
        ('obs_60_12',               '60 Min Observation — 12:00'),
        ('obs_60_13',               '60 Min Observation — 13:00'),
        ('obs_60_14',               '60 Min Observation — 14:00'),
        ('obs_60_15',               '60 Min Observation — 15:00'),
        ('obs_60_16',               '60 Min Observation — 16:00'),
        ('obs_60_17',               '60 Min Observation — 17:00'),
        ('obs_60_18',               '60 Min Observation — 18:00'),
        ('obs_60_19',               '60 Min Observation — 19:00'),
        ('obs_60_20',               '60 Min Observation — 20:00'),
        ('obs_60_21',               '60 Min Observation — 21:00'),
        ('obs_60_22',               '60 Min Observation — 22:00'),
        ('obs_60_23',               '60 Min Observation — 23:00'),
        ('obs_60_00',               '60 Min Observation — 00:00'),
        ('obs_60_01',               '60 Min Observation — 01:00'),
        ('obs_60_02',               '60 Min Observation — 02:00'),
        ('obs_60_03',               '60 Min Observation — 03:00'),
        ('obs_60_04',               '60 Min Observation — 04:00'),
        ('obs_60_05',               '60 Min Observation — 05:00'),
        ('obs_60_06',               '60 Min Observation — 06:00'),
        ('temperature_check',       'Temperature Check'),
        ('blood_pressure_check',    'Blood Pressure Check'),
        ('pulse_check',             'Pulse / Heart Rate Check'),
        ('oxygen_saturation_check', 'Oxygen Saturation (SpO2) Check'),
        ('respiration_rate_check',  'Respiratory Rate Check'),
        ('pain_assessment',         'Pain Assessment'),
        # ── PERSONAL CARE ─────────────────────────────────────────────────
        ('morning_wash',            'Morning Wash'),
        ('bed_bath',                'Full Bed Bath'),
        ('shower_assistance',       'Shower Assistance'),
        ('oral_care',               'Oral Care (Morning)'),
        ('oral_care_pm',            'Oral Care (Evening)'),
        ('hair_care',               'Hair Care / Grooming'),
        ('shaving_assistance',      'Shaving Assistance'),
        ('nail_care',               'Nail Care'),
        ('dressing_assistance',     'Dressing Assistance'),
        ('evening_wash',            'Evening Wash / Freshen Up'),
        ('continence_pad_change',   'Continence Pad Change'),
        ('toileting_assistance',    'Toileting Assistance'),
        ('perineal_care',           'Perineal Care'),
        # ── MEDICATION ────────────────────────────────────────────────────
        ('morning_meds',            'Morning Medications'),
        ('lunch_meds',              'Lunchtime Medications'),
        ('evening_meds',            'Evening Medications'),
        ('night_meds',              'Night Medications'),
        ('prn_medication',          'PRN Medication (As Required)'),
        ('medication_round_check',  'Medication Round Check'),
        ('medication_refusal_record','Medication Refusal Record'),
        ('controlled_drug_check',   'Controlled Drug Check'),
        # ── NUTRITION & HYDRATION ─────────────────────────────────────────
        ('breakfast',               'Breakfast'),
        ('lunch',                   'Lunch'),
        ('dinner',                  'Dinner'),
        ('afternoon_tea',           'Afternoon Tea & Snack'),
        ('assist_feeding',          'Feeding Assistance'),
        ('record_food_intake',      'Food Intake Record'),
        ('monitor_swallowing',      'Swallowing / Dysphagia Monitoring'),
        ('hydration_check',         'Hydration Check'),
        ('fluid_intake_record',     'Fluid Intake Record'),
        ('encourage_fluids',        'Encourage Fluids'),
        ('nutritional_supplement',  'Nutritional Supplement'),
        ('special_diet_check',      'Special Diet Check'),
        # ── MOBILITY & PHYSICAL ───────────────────────────────────────────
        ('mobility_assistance',     'Mobility Assistance'),
        ('walking_support',         'Walking Support'),
        ('wheelchair_transfer',     'Wheelchair Transfer'),
        ('bed_to_chair_transfer',   'Bed to Chair Transfer'),
        ('physiotherapy_exercises', 'Physiotherapy Exercises'),
        ('mobility_assessment',     'Mobility Assessment'),
        ('fall_risk_monitoring',    'Fall Risk Monitoring'),
        ('repositioning_pm',        'Repositioning / Turning (PM)'),
        ('repositioning_night',     'Repositioning / Turning (Night)'),
        ('pressure_care_am',        'Pressure Area Care (AM)'),
        ('pressure_care_pm',        'Pressure Area Care (PM)'),
        # ── SKIN & WOUND CARE ─────────────────────────────────────────────
        ('skin_integrity_check',    'Skin Integrity Check'),
        ('pressure_area_check',     'Pressure Area Check'),
        ('apply_barrier_cream',     'Apply Barrier / Moisturising Cream'),
        ('inspect_wounds',          'Inspect Wounds'),
        ('dressing_change',         'Dressing Change'),
        ('wound_care',              'Wound Care'),
        ('pressure_ulcer_monitoring','Pressure Ulcer Monitoring'),
        # ── MENTAL WELLBEING & ACTIVITIES ────────────────────────────────
        ('wellbeing_check',         'Wellbeing Check'),
        ('mood_observation',        'Mood Observation'),
        ('cognitive_stimulation',   'Cognitive Stimulation'),
        ('engage_social_activity',  'Social Activity / Engagement'),
        ('music_therapy',           'Music Therapy'),
        ('reading_activity',        'Reading / Story Time'),
        ('group_activity',          'Group Activity'),
        ('one_to_one_conversation', 'One-to-One Conversation'),
        # ── SLEEP & NIGHT MONITORING ──────────────────────────────────────
        ('sleep_check',             'Sleep Check'),
        ('night_round_check',       'Night Round Check'),
        ('restlessness_monitoring', 'Restlessness Monitoring'),
        ('sleep_pattern_record',    'Sleep Pattern Record'),
        ('comfort_check',           'Comfort Check'),
        ('bed_position_check',      'Bed Position Check'),
        # ── INFECTION CONTROL ─────────────────────────────────────────────
        ('infection_symptom_check', 'Infection Symptom Check'),
        ('temperature_monitoring',  'Temperature Monitoring'),
        ('ppe_compliance_check',    'PPE Compliance Check'),
        ('hand_hygiene_check',      'Hand Hygiene Check'),
        ('isolation_precaution_check','Isolation Precaution Check'),
        ('room_cleanliness_check',  'Room Cleanliness Check'),
        # ── SAFETY & ENVIRONMENT ──────────────────────────────────────────
        ('bed_rails_check',         'Bed Rails Check'),
        ('call_bell_check',         'Call Bell Check'),
        ('room_safety_check',       'Room Safety Check'),
        ('trip_hazard_check',       'Trip Hazard Check'),
        ('lighting_check',          'Lighting Check'),
        ('fire_exit_check',         'Fire Exit Check'),
        ('emergency_equipment_check','Emergency Equipment Check'),
        # ── FAMILY & COMMUNICATION ────────────────────────────────────────
        ('family_update_call',      'Family Update Call'),
        ('visitor_log',             'Visitor Log'),
        ('family_concern_followup', 'Family Concern Follow-up'),
        ('care_plan_review',        'Care Plan Review'),
        ('handover_note',           'Shift Handover Note'),
        ('incident_report',         'Incident Report'),
    ]

    patient      = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tasks')
    task_type    = models.CharField(max_length=40, choices=TASK_CHOICES)
    shift        = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    priority     = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date     = models.DateField(default=timezone.now)
    due_time     = models.CharField(max_length=5, blank=True, help_text='HH:MM')
    completed    = models.BooleanField(default=False)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_completed')
    completed_at = models.DateTimeField(null=True, blank=True)
    notes        = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['due_date', 'due_time', 'task_type']
        unique_together = ['patient', 'task_type', 'due_date']

    def __str__(self):
        return f'{self.get_task_type_display()} for {self.patient} on {self.due_date}'

    @property
    def is_overdue(self):
        if self.completed:
            return False
        return self.due_date < timezone.now().date()

    @property
    def priority_color(self):
        return {'high': 'danger', 'medium': 'warning', 'low': 'success'}.get(self.priority, 'secondary')

    @property
    def priority_icon(self):
        return {'high': 'bi-exclamation-triangle-fill', 'medium': 'bi-dash-circle-fill', 'low': 'bi-check-circle-fill'}.get(self.priority, 'bi-circle')

    @property
    def shift_color(self):
        return {'morning': 'warning', 'afternoon': 'primary', 'night': 'dark'}.get(self.shift, 'secondary')

    @property
    def category(self):
        obs = ['obs_60_07','obs_60_08','obs_60_09','obs_60_10','obs_60_11','obs_60_12',
               'obs_60_13','obs_60_14','obs_60_15','obs_60_16','obs_60_17','obs_60_18',
               'obs_60_19','obs_60_20','obs_60_21','obs_60_22','obs_60_23','obs_60_00',
               'obs_60_01','obs_60_02','obs_60_03','obs_60_04','obs_60_05','obs_60_06',
               'temperature_check','blood_pressure_check','pulse_check',
               'oxygen_saturation_check','respiration_rate_check','pain_assessment']
        personal = ['morning_wash','bed_bath','shower_assistance','oral_care','oral_care_pm',
                    'hair_care','shaving_assistance','nail_care','dressing_assistance',
                    'evening_wash','continence_pad_change','toileting_assistance','perineal_care']
        meds = ['morning_meds','lunch_meds','evening_meds','night_meds','prn_medication',
                'medication_round_check','medication_refusal_record','controlled_drug_check']
        nutrition = ['breakfast','lunch','dinner','afternoon_tea','assist_feeding',
                     'record_food_intake','monitor_swallowing','hydration_check',
                     'fluid_intake_record','encourage_fluids','nutritional_supplement','special_diet_check']
        mobility = ['mobility_assistance','walking_support','wheelchair_transfer',
                    'bed_to_chair_transfer','physiotherapy_exercises','mobility_assessment',
                    'fall_risk_monitoring','repositioning_pm','repositioning_night',
                    'pressure_care_am','pressure_care_pm']
        skin = ['skin_integrity_check','pressure_area_check','apply_barrier_cream',
                'inspect_wounds','dressing_change','wound_care','pressure_ulcer_monitoring']
        wellbeing = ['wellbeing_check','mood_observation','cognitive_stimulation',
                     'engage_social_activity','music_therapy','reading_activity',
                     'group_activity','one_to_one_conversation']
        sleep = ['sleep_check','night_round_check','restlessness_monitoring',
                 'sleep_pattern_record','comfort_check','bed_position_check']
        infection = ['infection_symptom_check','temperature_monitoring','ppe_compliance_check',
                     'hand_hygiene_check','isolation_precaution_check','room_cleanliness_check']
        safety = ['bed_rails_check','call_bell_check','room_safety_check','trip_hazard_check',
                  'lighting_check','fire_exit_check','emergency_equipment_check']
        family = ['family_update_call','visitor_log','family_concern_followup',
                  'care_plan_review','handover_note','incident_report']
        if self.task_type in obs:      return 'Observation'
        if self.task_type in personal: return 'Personal Care'
        if self.task_type in meds:     return 'Medication'
        if self.task_type in nutrition:return 'Nutrition'
        if self.task_type in mobility: return 'Mobility'
        if self.task_type in skin:     return 'Skin Care'
        if self.task_type in wellbeing:return 'Wellbeing'
        if self.task_type in sleep:    return 'Sleep'
        if self.task_type in infection:return 'Infection Control'
        if self.task_type in safety:   return 'Safety'
        if self.task_type in family:   return 'Communication'
        return 'General'

    @property
    def category_icon(self):
        icons = {
            'Observation': 'bi-eye',
            'Personal Care': 'bi-droplet',
            'Medication': 'bi-capsule',
            'Nutrition': 'bi-cup-hot',
            'Mobility': 'bi-person-walking',
            'Skin Care': 'bi-bandaid',
            'Wellbeing': 'bi-emoji-smile',
            'Sleep': 'bi-moon-stars',
            'Infection Control': 'bi-shield-check',
            'Safety': 'bi-shield-exclamation',
            'Communication': 'bi-telephone',
        }
        return icons.get(self.category, 'bi-check-circle')