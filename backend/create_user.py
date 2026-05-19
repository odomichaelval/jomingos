import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Jomingos.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

User.objects.create_superuser(
    username="admin",
    email="admin@test.com",
    password="Admin12345!"
)

print("User created")