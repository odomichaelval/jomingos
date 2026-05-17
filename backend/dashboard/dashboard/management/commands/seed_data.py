"""
Seed demo data for Jomingos
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import User
from patients.models import Patient
from care_notes.models import CareNote
from medications.models import Medication
from vitals.models import VitalSigns
import random


class Command(BaseCommand):
    help = 'Seeds Jomingos with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding Jomingos demo data...')

        # Create staff
        admin = User.objects.create_superuser(
            username='admin', password='admin123',
            first_name='Sarah', last_name='Thompson',
            email='admin@Jomingos.com', role='admin',
            job_title='Care Home Manager'
        )
        nurse1 = User.objects.create_user(
            username='nurse.adams', password='nurse123',
            first_name='Rachel', last_name='Adams',
            email='r.adams@Jomingos.com', role='nurse',
            job_title='Registered Nurse', is_on_duty=True
        )
        nurse2 = User.objects.create_user(
            username='nurse.patel', password='nurse123',
            first_name='Priya', last_name='Patel',
            email='p.patel@Jomingos.com', role='nurse',
            job_title='Senior Nurse'
        )
        doctor = User.objects.create_user(
            username='dr.wilson', password='doc123',
            first_name='James', last_name='Wilson',
            email='j.wilson@Jomingos.com', role='doctor',
            job_title='GP Consultant'
        )
        ca1 = User.objects.create_user(
            username='care.jones', password='care123',
            first_name='Emma', last_name='Jones',
            email='e.jones@Jomingos.com', role='care_assistant',
            job_title='Care Assistant', is_on_duty=True
        )
        self.stdout.write('  ✅ Created 5 staff accounts')

        # Create patients
        patients_data = [
            {'first_name': 'Margaret', 'last_name': 'Davies', 'dob': date(1938, 3, 15),
             'room': '101', 'care_level': 'nursing', 'gender': 'F',
             'allergies': 'Penicillin, Aspirin', 'nhs': '123 456 7890',
             'conditions': 'Type 2 Diabetes, Hypertension', 'blood': 'O+'},
            {'first_name': 'Arthur', 'last_name': 'Bennett', 'dob': date(1932, 7, 22),
             'room': '102', 'care_level': 'dementia', 'gender': 'M',
             'allergies': '', 'nhs': '234 567 8901',
             'conditions': 'Alzheimer\'s Disease (moderate), Osteoporosis', 'blood': 'A+'},
            {'first_name': 'Edith', 'last_name': 'Morrison', 'dob': date(1941, 11, 8),
             'room': '103', 'care_level': 'residential', 'gender': 'F',
             'allergies': 'Codeine', 'nhs': '345 678 9012',
             'conditions': 'Osteoarthritis, Mild depression', 'blood': 'B+'},
            {'first_name': 'Harold', 'last_name': 'Clarke', 'dob': date(1935, 5, 30),
             'room': '104', 'care_level': 'nursing', 'gender': 'M',
             'allergies': '', 'nhs': '456 789 0123',
             'conditions': 'COPD, Heart failure (Grade II)', 'blood': 'AB+'},
            {'first_name': 'Dorothy', 'last_name': 'Hughes', 'dob': date(1943, 9, 14),
             'room': '105', 'care_level': 'palliative', 'gender': 'F',
             'allergies': 'NSAIDs, Latex', 'nhs': '567 890 1234',
             'conditions': 'Advanced lung cancer, Chronic pain', 'blood': 'O-'},
            {'first_name': 'Frederick', 'last_name': 'Wilson', 'dob': date(1929, 1, 3),
             'room': '106', 'care_level': 'dementia', 'gender': 'M',
             'allergies': '', 'nhs': '678 901 2345',
             'conditions': 'Vascular dementia, Parkinson\'s disease', 'blood': 'A-'},
        ]

        patients = []
        for pd in patients_data:
            p = Patient.objects.create(
                first_name=pd['first_name'], last_name=pd['last_name'],
                date_of_birth=pd['dob'], gender=pd['gender'],
                nhs_number=pd['nhs'], blood_group=pd['blood'],
                room_number=pd['room'], care_level=pd['care_level'],
                admission_date=date.today() - timedelta(days=random.randint(30, 365)),
                allergies=pd['allergies'], medical_conditions=pd['conditions'],
                primary_nurse=nurse1, created_by=admin,
                emergency_contact_name='Family Contact',
                emergency_contact_phone='07700 900000',
                gp_name='Dr James Wilson', gp_phone='01234 567890',
                dietary_requirements='Low salt diet' if random.random() > 0.5 else '',
            )
            patients.append(p)
        self.stdout.write(f'  ✅ Created {len(patients)} patients')

        # Create care notes
        note_texts = [
            ('personal_care', 'Patient washed and dressed with assistance. Skin intact. No areas of concern noted. Patient cooperative throughout.'),
            ('nutrition', 'Breakfast consumed well — full bowl of porridge and orange juice. Good oral intake today. No swallowing difficulties observed.'),
            ('clinical', 'Patient reported increased pain in left hip this morning. Pain score 7/10. PRN paracetamol administered. Will monitor and escalate if no improvement.'),
            ('wellbeing', 'Patient appeared anxious during morning. Spent time reassuring. Family visited in afternoon — patient\'s mood improved significantly.'),
            ('activity', 'Participated in group exercise session. Engaged well with staff and other residents. Enjoyed afternoon bingo activity.'),
            ('sleep', 'Restless night — awoke three times. No apparent cause. Offered warm drink at 03:00. Settled by 04:00.'),
            ('continence', 'Continent throughout shift. No episodes of incontinence. Prompted to toilet every 2 hours as per care plan.'),
            ('clinical', 'Observed mild confusion this afternoon — more than baseline. Checked observations — all within normal limits. Fluids encouraged. Family notified.'),
        ]
        for patient in patients:
            for i, (cat, text) in enumerate(note_texts[:4]):
                CareNote.objects.create(
                    patient=patient, author=random.choice([nurse1, nurse2, ca1]),
                    category=cat,
                    priority=random.choice(['routine', 'routine', 'important']),
                    note_text=text,
                    created_at=timezone.now() - timedelta(hours=random.randint(1, 48))
                )
        self.stdout.write('  ✅ Created care notes')

        # Create medications
        meds_list = [
            ('Paracetamol', '500mg', 'oral', 'regular', 'Pain management'),
            ('Amlodipine', '5mg', 'oral', 'regular', 'Hypertension'),
            ('Metformin', '500mg', 'oral', 'regular', 'Type 2 diabetes'),
            ('Omeprazole', '20mg', 'oral', 'regular', 'Gastric protection'),
            ('Morphine Sulphate', '5mg', 'oral', 'prn', 'Breakthrough pain'),
            ('Salbutamol', '100mcg', 'inhaled', 'prn', 'Bronchospasm'),
            ('Furosemide', '40mg', 'oral', 'regular', 'Heart failure'),
        ]
        for patient in patients:
            for drug, dose, route, mtype, reason in random.sample(meds_list, 3):
                Medication.objects.create(
                    patient=patient, administered_by=random.choice([nurse1, nurse2]),
                    drug_name=drug, dosage=dose, route=route, med_type=mtype,
                    reason=reason,
                    administered_at=timezone.now() - timedelta(hours=random.randint(1, 24)),
                    witnessed_by='Care Assistant on duty',
                )
        self.stdout.write('  ✅ Created medication records')

        # Create vitals
        for patient in patients:
            for i in range(3):
                VitalSigns.objects.create(
                    patient=patient,
                    recorded_by=random.choice([nurse1, nurse2]),
                    temperature=round(random.uniform(36.0, 37.8), 1),
                    bp_systolic=random.randint(105, 145),
                    bp_diastolic=random.randint(65, 90),
                    heart_rate=random.randint(58, 98),
                    respiratory_rate=random.randint(14, 20),
                    oxygen_saturation=round(random.uniform(94.0, 99.5), 1),
                    blood_glucose=round(random.uniform(4.5, 9.0), 1),
                    weight_kg=round(random.uniform(55.0, 85.0), 1),
                    pain_score=random.randint(0, 5),
                    recorded_at=timezone.now() - timedelta(hours=random.randint(1, 72)),
                )
        self.stdout.write('  ✅ Created vital signs records')

        self.stdout.write(self.style.SUCCESS('\n🎉 Jomingos demo data seeded successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Nurse:    nurse.adams / nurse123')
        self.stdout.write('  Doctor:   dr.wilson / doc123')
        self.stdout.write('  Carer:    care.jones / care123')
