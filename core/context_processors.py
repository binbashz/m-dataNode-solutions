# context_processors.py

#que las notificaciones estén disponibles en todas las plantillas.

from .models import Notificacion

def notificaciones(request):
    if request.user.is_authenticated:
        notificaciones_usuario = Notificacion.objects.filter(usuario=request.user, leido=False)
        return {'notificaciones_usuario': notificaciones_usuario}
    return {'notificaciones_usuario': None}
