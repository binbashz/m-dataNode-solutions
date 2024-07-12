# tasks.py inicar sheduler tareas programadas.

from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.conf import settings
from .models import Pedido, Notificacion
import datetime
from datetime import timedelta
# Crear una instancia del scheduler 
scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

# Agregar el jobstore de Django 
scheduler.add_jobstore(DjangoJobStore(), "default")

def check_pedidos():
    now = timezone.now()
    deadline = now + timedelta(days=1)
    pedidos = Pedido.objects.filter(fecha_entrega__range=(now, deadline), estado='pendiente')
    
    for pedido in pedidos:
        if not Notificacion.objects.filter(pedido=pedido).exists():
            mensaje = f"El pedido #{pedido.id} de {pedido.producto} está programado para ser entregado mañana."
            Notificacion.objects.create(
                usuario=pedido.usuario,
                pedido=pedido,
                mensaje=mensaje
            )

def iniciar_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(check_pedidos, 'interval', minutes=30, name='check_pedidos', jobstore='default')
    scheduler.start()
    print("Scheduler iniciado. Tareas programadas en ejecución.")
    