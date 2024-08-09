from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Pedido, Notificacion
from datetime import timedelta

scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
scheduler.add_jobstore(DjangoJobStore(), "default")

def check_pedidos():
    print("Ejecutando check_pedidos...")  # Para depuración
    hoy = timezone.now().date()
    manana = hoy + timedelta(days=1)
    
    # Pedidos que vencen mañana
    pedidos_manana = Pedido.objects.filter(fecha_entrega=manana, estado='pendiente')
    for pedido in pedidos_manana:
        Notificacion.objects.get_or_create(
            usuario=pedido.usuario,
            pedido=pedido,
            defaults={'mensaje': f"Tu pedido {pedido.id} está programado para ser entregado mañana."}
        )

    # Pedidos que vencen hoy
    pedidos_hoy = Pedido.objects.filter(fecha_entrega=hoy, estado='pendiente')
    for pedido in pedidos_hoy:
        Notificacion.objects.get_or_create(
            usuario=pedido.usuario,
            pedido=pedido,
            defaults={'mensaje': f"Tu pedido {pedido.id} debe ser entregado hoy."}
        )

    # Eliminar notificaciones de pedidos completados o cancelados
    Notificacion.objects.filter(pedido__estado__in=['completado', 'cancelado']).delete()

def iniciar_scheduler():
    scheduler.add_job(check_pedidos, 'interval', minutes=5, name='check_pedidos', jobstore='default')
    scheduler.start()
    print("Scheduler iniciado. Tareas programadas en ejecución.")

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
    

