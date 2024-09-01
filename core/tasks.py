from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Pedido, Notificacion
from datetime import timedelta
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

# Configura el scheduler para usar la zona horaria de Django
scheduler = BackgroundScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})
scheduler.add_jobstore(DjangoJobStore(), "default")

def check_pedidos():
    logger.info("Iniciando check_pedidos")
    start_time = timezone.now()
    try:
        hoy = timezone.now().date()
        manana = hoy + timedelta(days=1)
        
        # Combina las consultas para reducir el número de operaciones de base de datos
        pedidos = Pedido.objects.filter(
            Q(fecha_entrega=hoy) | Q(fecha_entrega=manana),
            estado='pendiente'
        )
        
        for pedido in pedidos:
            mensaje = f"Tu pedido {pedido.id} está programado para ser entregado {'hoy' if pedido.fecha_entrega == hoy else 'mañana'}."
            Notificacion.objects.get_or_create(
                usuario=pedido.usuario,
                pedido=pedido,
                defaults={'mensaje': mensaje}
            )

        # Eliminar notificaciones de pedidos completados o cancelados
        Notificacion.objects.filter(pedido__estado__in=['completado', 'cancelado']).delete()
        
        logger.info("check_pedidos completado exitosamente")
    except Exception as e:
        logger.error(f"Error en check_pedidos: {str(e)}")
    finally:
        end_time = timezone.now()
        logger.info(f"Tiempo de ejecución de check_pedidos: {end_time - start_time}")

def iniciar_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            check_pedidos, 
            'interval', 
            minutes=5, 
            id='check_pedidos',
            replace_existing=True,
            misfire_grace_time=300  # 5 minutos de gracia
        )
        scheduler.start()
        logger.info("Scheduler iniciado. Tareas programadas en ejecución.")
    else:
        logger.info("El scheduler ya está en ejecución.")