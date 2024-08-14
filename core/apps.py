from django.apps import AppConfig
import os
from django.utils import timezone
from datetime import timedelta

scheduler_started = False

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        global scheduler_started
        if not scheduler_started and os.environ.get('RUN_MAIN') != 'true':
            from django.core.management import call_command
            from threading import Timer
            
            def delayed_start():
                from .tasks import iniciar_scheduler
                iniciar_scheduler()
                global scheduler_started
                scheduler_started = True
            
            # Retrasa el inicio del scheduler por 1 minuto
            Timer(60, delayed_start).start()