from django.core.management.base import BaseCommand

from accounts.models import User


DEMO_USERS = [
    {
        "username": "admin",
        "password": "admin123",
        "first_name": "Sarah",
        "last_name": "Thompson",
        "email": "admin@jomingos.local",
        "role": "admin",
        "job_title": "Care Home Manager",
        "is_staff": True,
        "is_superuser": True,
    },
    {
        "username": "nurse.adams",
        "password": "nurse123",
        "first_name": "Rachel",
        "last_name": "Adams",
        "email": "nurse.adams@jomingos.local",
        "role": "nurse",
        "job_title": "Registered Nurse",
        "is_on_duty": True,
    },
    {
        "username": "dr.wilson",
        "password": "doc123",
        "first_name": "James",
        "last_name": "Wilson",
        "email": "dr.wilson@jomingos.local",
        "role": "doctor",
        "job_title": "GP Consultant",
    },
    {
        "username": "care.jones",
        "password": "care123",
        "first_name": "Emma",
        "last_name": "Jones",
        "email": "care.jones@jomingos.local",
        "role": "care_assistant",
        "job_title": "Care Assistant",
        "is_on_duty": True,
    },
]


class Command(BaseCommand):
    help = "Create or update the fixed role-demo users used by the login page."

    def handle(self, *args, **options):
        for demo_user in DEMO_USERS:
            data = demo_user.copy()
            password = data.pop("password")
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults=data,
            )
            if not created:
                for field, value in data.items():
                    setattr(user, field, value)
            user.set_password(password)
            user.is_active = True
            user.save()

            status = "created" if created else "updated"
            self.stdout.write(f"{status}: {user.username} ({user.get_role_display()})")

        self.stdout.write(self.style.SUCCESS("Demo role users are ready."))
