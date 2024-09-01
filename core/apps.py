from django.apps import AppConfig
import os
from django.utils import timezone
from datetime import timedelta
import threading

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            from .tasks import iniciar_scheduler
            
            def delayed_start():
                # Espera a que la base de datos esté disponible
                threading.Timer(60, iniciar_scheduler).start()
            
            # Inicia el hilo
            threading.Thread(target=delayed_start).start()