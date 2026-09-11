import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from patients.models import Patient
from vitals.models import VitalSigns
from medications.models import Medication
from care_notes.models import CareNote


DRUG_POOL = [
    ('Paracetamol', '500mg', 'oral', 'regular', 'Pain relief'),
    ('Amlodipine', '5mg', 'oral', 'regular', 'Hypertension management'),
    ('Metformin', '500mg', 'oral', 'regular', 'Type 2 Diabetes management'),
    ('Furosemide', '40mg', 'oral', 'regular', 'Fluid retention'),
    ('Omeprazole', '20mg', 'oral', 'regular', 'Acid reflux'),
    ('Salbutamol', '100mcg', 'inhaled', 'prn', 'Breathlessness'),
    ('Morphine Sulfate', '10mg', 'oral', 'prn', 'Breakthrough pain'),
    ('Warfarin', '3mg', 'oral', 'regular', 'Anticoagulation'),
    ('Insulin Glargine', '10 units', 'sc', 'regular', 'Diabetes management'),
    ('Co-codamol', '30/500mg', 'oral', 'prn', 'Moderate pain'),
    ('Sertraline', '50mg', 'oral', 'regular', 'Low mood / anxiety'),
    ('Donepezil', '5mg', 'oral', 'regular', "Alzheimer's management"),
    ('Senna', '15mg', 'oral', 'prn', 'Constipation'),
    ('Diazepam', '2mg', 'oral', 'prn', 'Agitation'),
    ('Amoxicillin', '500mg', 'oral', 'stat', 'Suspected infection'),
]

# Realistic note text per category — deliberately varied wording so the
# summarisation/evaluation pipeline has genuine diversity to work with,
# not repeated identical sentences.
CATEGORY_NOTE_TEMPLATES = {
    'nutrition': [
        "Resident was assisted with {meal} at {time}. Ate approximately {amount} of the meal. No swallowing difficulties observed.",
        "Resident declined {meal}, stating they were not hungry. Offered an alternative snack, which was partially accepted.",
        "Resident required full assistance with {meal}. Ate well and appeared to enjoy the meal.",
    ],
    'hydration': [
        "Resident was offered fluids throughout the shift. Fluid intake recorded as {level} for the day.",
        "Resident drank a full glass of water without prompting. Hydration levels appear adequate.",
        "Resident was reluctant to drink fluids this shift. Encouraged regularly, intake remained {level}.",
    ],
    'personal_care': [
        "Resident was assisted with washing and dressing this morning. Skin checked, no areas of concern noted.",
        "Resident received a full bed bath. Pressure areas intact, no redness observed.",
        "Resident declined personal care this morning, will offer again later in the shift.",
    ],
    'mobility': [
        "Resident mobilised to the lounge with the assistance of a zimmer frame. No unsteadiness observed.",
        "Resident required two staff assist to transfer from bed to chair. Mobility appears reduced since last week.",
        "Resident walked independently to the dining room. Gait steady, no falls risk behaviour observed.",
    ],
    'emotional': [
        "Resident appeared settled and content throughout the shift, engaging well with staff and other residents.",
        "Resident was tearful this afternoon, expressing that they missed their family. Staff provided reassurance and comfort.",
        "Resident appeared anxious around mealtimes. Reassured by staff and settled after some time.",
    ],
    'sleep': [
        "Resident reported a good night's sleep, waking refreshed this morning.",
        "Resident was awake for much of the night, appeared restless. Will monitor over coming nights.",
        "Resident took a short nap in the afternoon after a poor night's sleep.",
    ],
    'observation_30': [
        "30-minute observation completed. Resident found resting comfortably in their room.",
        "30-minute observation completed. Resident awake and engaged in activity in the lounge.",
        "30-minute observation completed. Resident appeared settled, no concerns noted.",
    ],
    'handover': [
        "Handover note: resident had a settled shift overall, no concerns to escalate to the next team.",
        "Handover note: resident's appetite has been reduced over the past two days, to monitor at mealtimes.",
        "Handover note: resident requested to see the GP regarding ongoing joint pain, family have been informed.",
    ],
    'social': [
        "Resident enjoyed a visit from a family member this afternoon and appeared in good spirits afterward.",
        "Resident took part in the afternoon activity session, engaging well with other residents.",
        "Resident preferred to stay in their room today rather than join group activities.",
    ],
    'behaviour': [
        "Resident became briefly agitated during personal care, calmed with reassurance from staff.",
        "Resident was verbally aggressive towards a member of staff during medication rounds. De-escalated without incident.",
    ],
}

# Weighted so common, routine categories dominate, with occasional
# incident-type entries, mirroring realistic shift documentation patterns.
CATEGORY_WEIGHTS = [
    ('nutrition', 15), ('hydration', 10), ('personal_care', 15), ('mobility', 12),
    ('emotional', 12), ('sleep', 10), ('observation_30', 10), ('handover', 8),
    ('social', 6), ('behaviour', 2),
]

MEAL_POOL = ['breakfast', 'lunch', 'dinner', 'afternoon tea']
AMOUNT_POOL = ['all', 'most', 'about half', 'a small amount']
LEVEL_POOL = ['good', 'adequate', 'poor']


class Command(BaseCommand):
    help = 'Generates dummy vitals, medications, and care notes for a range of existing patients.'

    def add_arguments(self, parser):
        parser.add_argument('--start-id', type=int, default=11, help='First patient ID to populate (default: 11)')
        parser.add_argument('--end-id', type=int, default=100, help='Last patient ID to populate (default: 100)')
        parser.add_argument('--entries', type=int, default=10, help='Entries per patient per model (default: 10)')

    def handle(self, *args, **options):
        start_id = options['start_id']
        end_id = options['end_id']
        entries = options['entries']

        patients = Patient.objects.filter(pk__gte=start_id, pk__lte=end_id)
        staff = list(User.objects.all())

        if not patients.exists():
            self.stdout.write(self.style.ERROR('No patients found in that ID range.'))
            return
        if not staff:
            self.stdout.write(self.style.ERROR('No staff users found — cannot assign recorded_by/author.'))
            return

        def random_datetime_within(days_back):
            dt = timezone.now() - timedelta(days=random.randint(0, days_back))
            return dt.replace(
                hour=random.randint(6, 22),
                minute=random.choice([0, 15, 30, 45]),
                second=0, microsecond=0,
            )

        vitals_created = meds_created = notes_created = 0

        for patient in patients:

            # --- Vitals ---
            for _ in range(entries):
                VitalSigns.objects.create(
                    patient=patient,
                    recorded_by=random.choice(staff),
                    temperature=round(random.uniform(35.8, 38.2), 1),
                    bp_systolic=random.randint(95, 160),
                    bp_diastolic=random.randint(55, 95),
                    heart_rate=random.randint(55, 105),
                    respiratory_rate=random.randint(12, 24),
                    oxygen_saturation=round(random.uniform(92.0, 99.5), 1),
                    blood_glucose=round(random.uniform(4.0, 9.5), 1),
                    weight_kg=round(random.uniform(50.0, 95.0), 1),
                    pain_score=random.choices([0, 1, 2, 3, 4, 5], weights=[40, 20, 15, 10, 10, 5])[0],
                    recorded_at=random_datetime_within(21),
                )
                vitals_created += 1

            # --- Medications ---
            for _ in range(entries):
                drug_name, dosage, route, med_type, reason = random.choice(DRUG_POOL)
                witness = random.choice(staff)
                Medication.objects.create(
                    patient=patient,
                    administered_by=random.choice(staff),
                    drug_name=drug_name,
                    dosage=dosage,
                    route=route,
                    med_type=med_type,
                    administered_at=random_datetime_within(21),
                    reason=reason,
                    witnessed_by=getattr(witness, 'get_full_name', lambda: '')() or witness.username,
                    refused=random.random() < 0.05,
                )
                meds_created += 1

            # --- Care Notes ---
            for _ in range(entries):
                category = random.choices(
                    population=[c for c, w in CATEGORY_WEIGHTS],
                    weights=[w for c, w in CATEGORY_WEIGHTS],
                    k=1
                )[0]
                priority = random.choices(
                    population=['routine', 'important', 'urgent'],
                    weights=[75, 20, 5],
                    k=1
                )[0]
                template = random.choice(CATEGORY_NOTE_TEMPLATES[category])
                note_text = template.format(
                    meal=random.choice(MEAL_POOL),
                    time=f'{random.randint(7, 19):02d}:{random.choice(["00", "15", "30", "45"])}',
                    amount=random.choice(AMOUNT_POOL),
                    level=random.choice(LEVEL_POOL),
                )

                CareNote.objects.create(
                    patient=patient,
                    author=random.choice(staff),
                    category=category,
                    priority=priority,
                    note_text=note_text,
                    created_at=random_datetime_within(21),
                )
                notes_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Created {vitals_created} vitals, {meds_created} medications, {notes_created} care notes '
            f'across {patients.count()} patients (IDs {start_id}\u2013{end_id}).'
        ))