from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Pedido, Notificacion
from datetime import timedelta

# Configura el scheduler para usar la zona horaria de Django
scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
scheduler.add_jobstore(DjangoJobStore(), "default")

def check_pedidos():
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
    # Programa la primera ejecución de check_pedidos para que ocurra 5 minutos después de iniciar el scheduler
    scheduler.add_job(check_pedidos, 'interval', minutes=5, next_run_time=timezone.now() + timedelta(minutes=1), name='check_pedidos', jobstore='default')
    scheduler.start()
    print("Scheduler iniciado. Tareas programadas en ejecución.")
