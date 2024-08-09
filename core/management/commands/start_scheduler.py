from django.core.management.base import BaseCommand
from core.tasks import iniciar_scheduler

class Command(BaseCommand):
    help = 'Inicia el scheduler de tareas programadas'

    def handle(self, *args, **options):
        iniciar_scheduler()
        self.stdout.write(self.style.SUCCESS('Scheduler iniciado exitosamente'))