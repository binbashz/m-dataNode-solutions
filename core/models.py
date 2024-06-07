from django.utils import timezone


from django.contrib.auth.models import User
from django.db import models

class Variedad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Valor predeterminado a None

    def save(self, *args, **kwargs):
        if self.user is None:
            # Asignar el usuario actualmente autenticado si no se proporciona uno
            self.user = kwargs.pop('user', None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def details(self):
        return f"Variedad: {self.nombre}, Descripción: {self.descripcion}, Usuario: {self.user.username}"


class CondicionesCultivo(models.Model):
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, related_name='condiciones')
    registro_fecha = models.DateField()
    temperatura = models.FloatField()
    humedad = models.FloatField()
    tipo_suelo = models.CharField(max_length=100)
    ph_suelo = models.FloatField(default=7.0) 
    nutrientes = models.CharField(max_length=100, default='normal')

    def __str__(self):
        return f"{self.variedad} - {self.registro_fecha}"


class TratamientoFitofarmaceutico(models.Model):
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, related_name='tratamientos_fitofarmaceuticos')
    tratamiento = models.CharField(max_length=200)
    fecha_aplicacion = models.DateField()
    dosis = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.variedad} - {self.tratamiento}"


class AnalisisCalidad(models.Model):
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, related_name='analisis')
    tipo_analisis = models.CharField(max_length=100)
    resultado = models.TextField()
    fecha_analisis = models.DateField()

    def __str__(self):
        return f"{self.tipo_analisis} - {self.variedad.nombre} - {self.fecha_analisis}"

    def details(self):
        return f"Análisis de {self.tipo_analisis} para {self.variedad.nombre}, Resultado: {self.resultado}, Fecha: {self.fecha_analisis}"
