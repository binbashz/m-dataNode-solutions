from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Variedad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 

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
    tipo_suelo = models.CharField(max_length=100, choices=[
        ('arcilloso', 'Arcilloso: Alta proporción de arcilla, retiene agua y nutrientes.'),
        ('arenoso', 'Arenoso: Mucha arena, muy permeable, retiene menos agua y nutrientes.'),
        ('limoso', 'Limoso: Textura suave, retiene agua y nutrientes.'),
        ('humifero', 'Humífero: Rico en materia orgánica y nutrientes, muy fértil.'),
        ('calcareo', 'Calcáreo: Alto contenido de calcio, afecta el pH del suelo.'),
        ('salino', 'Salino: Concentraciones altas de sales solubles, perjudicial para cultivos.'),
        ('turba', 'Turba: Suelo orgánico de descomposición vegetal.'),
    ])
    ph_suelo = models.FloatField(default=7.0)
    nutrientes = models.CharField(max_length=100, default='normal')
    iluminacion = models.FloatField(default=0.0)
    temperatura_suelo = models.FloatField(default=0.0)
    humedad_suelo = models.FloatField(default=0.0)
    temperatura_ambiente = models.FloatField(default=0.0)
    humedad_ambiente = models.FloatField(default=0.0)
    concentracion_co2 = models.FloatField(default=400.0)
    ventilacion = models.CharField(max_length=100, default='normal')
    oxigeno_suelo = models.FloatField(default=0.0)
    calidad_agua_ph = models.FloatField(default=6.0)
    calidad_agua_cloro = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.variedad} - {self.registro_fecha}"


class Cultivo(models.Model):
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE)
    cantidad_plantas = models.IntegerField()
    area_cultivo = models.FloatField(help_text="Área de cultivo en m²")
    luz_intensidad = models.FloatField(help_text="Intensidad de luz en lúmenes")
    luz_horas = models.FloatField(help_text="Horas de luz por día")
    temperatura_dia = models.FloatField(help_text="Temperatura durante el día en °C")
    humedad = models.FloatField(help_text="Humedad relativa en %")
    ph = models.FloatField(help_text="Nivel de pH del suelo")

    def __str__(self):
        return f"Cultivo de {self.variedad} con {self.cantidad_plantas} plantas"


class AnalisisCostos(models.Model):
    costo_semilla = models.FloatField()
    costo_sustrato = models.FloatField()
    costo_energia = models.FloatField()
    costo_agua = models.FloatField()
    costo_manobra = models.FloatField()
    presupuesto = models.FloatField()
    produccion_gramos = models.FloatField(blank=True, null=True)  

    def __str__(self):
        return f"Análisis de Costos {self.id}"


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


# Analisis
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class TipoAnalisis(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    metodo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Muestra(models.Model):
    codigo = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_analisis = models.ForeignKey(TipoAnalisis, on_delete=models.CASCADE, null=True, blank=True)
    fecha_recepcion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.codigo


class AnalisisProgramado(models.Model):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE)
    tipo_analisis = models.ForeignKey(TipoAnalisis, on_delete=models.CASCADE)
    fecha_programada = models.DateTimeField()
    prioridad = models.IntegerField(choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')])

    def __str__(self):
        return f"{self.tipo_analisis.nombre} - {self.muestra.codigo}"

class ResultadoAnalisis(models.Model):
    analisis_programado = models.ForeignKey(AnalisisProgramado, on_delete=models.CASCADE)
    fecha_analisis = models.DateTimeField()
    resultados = models.TextField() 
    observaciones = models.TextField(blank=True, null=True)

    # barcode model - codigo barras
class Product(models.Model):
    name = models.CharField(max_length=36)
    code = models.CharField(max_length=15, unique=True)
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name




class GastoOperativo(models.Model):
    TIPOS_GASTO = (
        ('Mantenimiento', 'Mantenimiento'),
        ('Suministros', 'Suministros'),
        ('Personal', 'Personal'),
        ('Otros', 'Otros'),
    )
    
    tipo_gasto = models.CharField(max_length=20, choices=TIPOS_GASTO)
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.tipo_gasto} - ${self.monto} ({self.variedad.nombre})'

   

class Venta(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return f'{self.producto} - {self.cantidad} unidades ({self.variedad.nombre})'

class Pedido(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    fecha_pedido = models.DateField()
    fecha_entrega = models.DateField()
    variedad = models.ForeignKey(Variedad, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f'{self.producto} - {self.cantidad} unidades ({self.variedad.nombre})'
