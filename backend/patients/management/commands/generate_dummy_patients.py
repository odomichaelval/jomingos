import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from patients.models import Patient


FIRST_NAMES_M = [
    'Arthur', 'George', 'Frederick', 'Albert', 'Harold', 'Leonard', 'Norman',
    'Stanley', 'Kenneth', 'Cyril', 'Wilfred', 'Reginald', 'Edwin', 'Bernard',
    'Douglas', 'Gerald', 'Ronald', 'Sidney', 'Victor', 'Horace',
]
FIRST_NAMES_F = [
    'Margaret', 'Dorothy', 'Elsie', 'Florence', 'Gladys', 'Edith', 'Winifred',
    'Doris', 'Hilda', 'Agnes', 'Muriel', 'Vera', 'Joan', 'Phyllis', 'Ivy',
    'Nora', 'Beatrice', 'Constance', 'Ethel', 'Marjorie',
]
LAST_NAMES = [
    'Whitfield', 'Armitage', 'Sutcliffe', 'Braithwaite', 'Sinclair', 'Fenwick',
    'Marsden', 'Tomlinson', 'Ashworth', 'Ogden', 'Hartley', 'Kershaw',
    'Ainsworth', 'Bamford', 'Crowther', 'Dyson', 'Heaton', 'Naylor',
    'Ridgway', 'Stansfield', 'Thornber', 'Wadsworth', 'Yeadon', 'Clough',
]

CARE_LEVEL_WEIGHTS = [
    ('residential', 40), ('nursing', 25), ('dementia', 20),
    ('respite', 10), ('palliative', 5),
]
ALLERGIES_POOL = [
    '', '', '', 'Penicillin', 'Latex', 'Peanuts', 'Sulphonamides',
    'Aspirin', 'Shellfish', 'Penicillin, Latex',
]
CONDITIONS_POOL = [
    'Type 2 Diabetes', 'Hypertension', 'Osteoarthritis', 'Atrial Fibrillation',
    'COPD', "Alzheimer's Disease", 'Vascular Dementia', 'Parkinson\'s Disease',
    'Chronic Kidney Disease', 'Osteoporosis', 'Depression', 'Anxiety',
]
DIETARY_POOL = [
    '', 'Diabetic diet', 'Soft/pureed diet', 'Gluten-free', 'Low sodium',
    'Thickened fluids', 'Vegetarian', 'Renal diet',
]
MOBILITY_POOL = [
    'Independent', 'Uses walking stick', 'Uses zimmer frame', 'Uses rollator',
    'Wheelchair user', 'Requires hoist', 'One staff assist', 'Bed-bound',
]
RELATION_POOL = ['Daughter', 'Son', 'Spouse', 'Niece', 'Nephew', 'Friend', 'Sister', 'Brother']


class Command(BaseCommand):
    help = 'Generates synthetic dummy patients for dissertation testing/evaluation purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=90,
            help='Number of dummy patients to generate (default: 90)'
        )

    def handle(self, *args, **options):
        count = options['count']

        existing_rooms = set(Patient.objects.values_list('room_number', flat=True))
        existing_nhs = set(Patient.objects.values_list('nhs_number', flat=True))

        nurses = list(User.objects.filter(role='nurse'))
        creator = User.objects.filter(is_superuser=True).first()

        created = 0
        attempts = 0

        while created < count and attempts < count * 3:
            attempts += 1

            gender = random.choice(['M', 'F'])
            first_name = random.choice(FIRST_NAMES_M if gender == 'M' else FIRST_NAMES_F)
            last_name = random.choice(LAST_NAMES)

            # Ages weighted toward realistic care-home range (65-99), some younger for respite
            age = random.choices(
                population=range(60, 101),
                weights=[1 if a < 65 else 3 for a in range(60, 101)],
                k=1
            )[0]
            dob = date.today() - timedelta(days=age * 365 + random.randint(0, 364))

            care_level = random.choices(
                population=[c for c, w in CARE_LEVEL_WEIGHTS],
                weights=[w for c, w in CARE_LEVEL_WEIGHTS],
                k=1
            )[0]

            # Unique-ish room number: Floor (1-3) + room (01-30)
            room_number = None
            for _ in range(20):
                candidate = f'{random.randint(1, 5)}{random.randint(1, 40):02d}'
                if candidate not in existing_rooms:
                    room_number = candidate
                    existing_rooms.add(candidate)
                    break
            if not room_number:
                continue  # skip this attempt if we couldn't find a free room number

            # Unique NHS number (fake, 10 digits)
            nhs_number = None
            for _ in range(20):
                candidate = ''.join(str(random.randint(0, 9)) for _ in range(10))
                if candidate not in existing_nhs:
                    nhs_number = candidate
                    existing_nhs.add(candidate)
                    break

            admission_date = date.today() - timedelta(days=random.randint(10, 1500))

            patient = Patient(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=dob,
                gender=gender,
                nhs_number=nhs_number,
                blood_group=random.choice([c for c, _ in Patient.BLOOD_GROUP_CHOICES] + ['']),
                room_number=room_number,
                admission_date=admission_date,
                care_level=care_level,
                primary_nurse=random.choice(nurses) if nurses and random.random() > 0.2 else None,
                allergies=random.choice(ALLERGIES_POOL),
                medical_conditions=', '.join(random.sample(CONDITIONS_POOL, k=random.randint(0, 3))),
                dietary_requirements=random.choice(DIETARY_POOL),
                mobility_status=random.choice(MOBILITY_POOL),
                emergency_contact_name=f'{random.choice(FIRST_NAMES_M + FIRST_NAMES_F)} {last_name}',
                emergency_contact_phone=f'07700 9{random.randint(0,0)}{random.randint(0,9999):04d}',
                emergency_contact_relation=random.choice(RELATION_POOL),
                gp_name=f"Dr. {random.choice(LAST_NAMES)}",
                gp_phone=f'0113 496 {random.randint(0,9999):04d}',
                is_active=True,
                created_by=creator,
            )
            patient.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created} dummy patients.'
        ))