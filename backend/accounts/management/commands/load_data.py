from django.core.management.base import BaseCommand
from django.core.management import call_command
from pathlib import Path

class Command(BaseCommand):
    help = "Load data.json into database"

    def handle(self, *args, **kwargs):
        file_path = Path("data.json")

        if not file_path.exists():
            self.stdout.write(self.style.ERROR("data.json not found"))
            return

        self.stdout.write("Loading data.json...")

        call_command("loaddata", "data.json")

        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))