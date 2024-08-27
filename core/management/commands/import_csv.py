import csv
import os
from django.core.management.base import BaseCommand
from core.models import CannabisPlant
from django.conf import settings

class Command(BaseCommand):
    help = 'Import cannabis data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CannabisPlant.objects.create(
                    strain=row['Strain'],
                    plant_type=row['Type'],
                    rating=row['Rating'],
                    effects=row['Effects'],
                    flavor=row['Flavor'],
                    description=row['Description'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
