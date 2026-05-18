from django.core.management.base import BaseCommand
from django.utils import timezone
from patients.models import Patient
from accounts.models import User
import random
from datetime import date

class Command(BaseCommand):
    help = 'Seed the database with test patient records'

    def handle(self, *args, **options):
        # Clear existing patients
        Patient.objects.all().delete()

        # Get a care staff member for contact
        care_staff = User.objects.filter(is_active=True).first()

        # Test patient data
        patients_data = [
            {
                'first_name': 'Margaret',
                'last_name': 'Johnson',
                'date_of_birth': date(1945, 3, 15),
                'nhs_number': 'NHS123456789',
                'room_number': '101',
                'care_level': 'nursing',
                'allergies': 'Penicillin, Codeine',
                'medical_conditions': 'Type 2 Diabetes, Hypertension, Arthritis',
            },
            {
                'first_name': 'Robert',
                'last_name': 'Smith',
                'date_of_birth': date(1940, 7, 22),
                'nhs_number': 'NHS987654321',
                'room_number': '102',
                'care_level': 'dementia',
                'allergies': 'Aspirin',
                'medical_conditions': 'Alzheimers Disease, Hypertension',
            },
            {
                'first_name': 'Elizabeth',
                'last_name': 'Williams',
                'date_of_birth': date(1952, 11, 8),
                'nhs_number': 'NHS456789123',
                'room_number': '103',
                'care_level': 'residential',
                'allergies': 'None known',
                'medical_conditions': 'COPD, Atrial Fibrillation',
            },
            {
                'first_name': 'James',
                'last_name': 'Brown',
                'date_of_birth': date(1948, 5, 3),
                'nhs_number': 'NHS789123456',
                'room_number': '104',
                'care_level': 'nursing',
                'allergies': 'Sulfamethoxazole',
                'medical_conditions': 'Chronic Kidney Disease, Diabetes',
            },
            {
                'first_name': 'Patricia',
                'last_name': 'Davis',
                'date_of_birth': date(1950, 2, 14),
                'nhs_number': 'NHS321654987',
                'room_number': '105',
                'care_level': 'residential',
                'allergies': 'Morphine',
                'medical_conditions': 'Osteoporosis, Heart Failure',
            },
            {
                'first_name': 'David',
                'last_name': 'Miller',
                'date_of_birth': date(1944, 9, 27),
                'nhs_number': 'NHS654987321',
                'room_number': '106',
                'care_level': 'dementia',
                'allergies': 'None known',
                'medical_conditions': 'Dementia, Parkinson Disease',
            },
            {
                'first_name': 'Jennifer',
                'last_name': 'Wilson',
                'date_of_birth': date(1946, 12, 1),
                'nhs_number': 'NHS147258369',
                'room_number': '107',
                'care_level': 'nursing',
                'allergies': 'Latex, Ibuprofen',
                'medical_conditions': 'Pneumonia History, Anemia',
            },
            {
                'first_name': 'Michael',
                'last_name': 'Moore',
                'date_of_birth': date(1949, 4, 10),
                'nhs_number': 'NHS258369147',
                'room_number': '108',
                'care_level': 'residential',
                'allergies': 'None known',
                'medical_conditions': 'Prostate Cancer History, Hypertension',
            },
            {
                'first_name': 'Linda',
                'last_name': 'Taylor',
                'date_of_birth': date(1947, 6, 19),
                'nhs_number': 'NHS369147258',
                'room_number': '109',
                'care_level': 'dementia',
                'allergies': 'Penicillin',
                'medical_conditions': 'Vascular Dementia, Depression',
            },
            {
                'first_name': 'Richard',
                'last_name': 'Anderson',
                'date_of_birth': date(1943, 1, 5),
                'nhs_number': 'NHS741852963',
                'room_number': '110',
                'care_level': 'nursing',
                'allergies': 'None known',
                'medical_conditions': 'Stroke History, Diabetes, Aphasia',
            },
        ]

        # Create patients
        created_count = 0
        for data in patients_data:
            patient, created = Patient.objects.get_or_create(
                nhs_number=data['nhs_number'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'date_of_birth': data['date_of_birth'],
                    'room_number': data['room_number'],
                    'care_level': data['care_level'],
                    'allergies': data['allergies'],
                    'medical_conditions': data['medical_conditions'],
                    'is_active': True,
                    'gender': random.choice(['M', 'F']),
                    'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                    'emergency_contact_name': 'Family Member',
                    'emergency_contact_phone': f"+44 7700 {random.randint(100000, 999999)}",
                    'emergency_contact_relation': 'Spouse',
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {created_count} patient records'
            )
        )
