from io import BytesIO
# Módulos de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.db.models import Count, Q
from django.contrib import messages
from django.utils.timezone import make_aware, get_current_timezone
from django.utils import timezone
from django.core.paginator import Paginator
# Reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Barcode y PIL
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

# Matplotlib
import matplotlib.pyplot as plt

# Python estándar
import base64
import urllib.parse
import io
import os

# Modelos y Formularios 
from .models import (
    Variedad, CondicionesCultivo, Cultivo, AnalisisCostos,
    TratamientoFitofarmaceutico, AnalisisCalidad, Cliente, 
    Muestra, TipoAnalisis, AnalisisProgramado, 
    ResultadoAnalisis, Product, Miembro, Cuota,Pago,
    GastoOperativo, Venta, Pedido, PlanProduccion,
    TareaProduccion, ListaMateriales, ItemListaMateriales, Material,CannabisPlant
)
from .forms import (
    RegisterForm, VariedadForm, CondicionesCultivoForm, TratamientoFitofarmaceuticoForm,
    AnalisisCalidadForm, CultivoForm, AnalisisCostosForm, ClienteForm,
    MuestraForm, AnalisisProgramadoForm, ResultadoAnalisisForm, GastoOperativoForm,
    VentaForm, PedidoForm, PlanProduccionForm, TareaProduccionForm,
    ListaMaterialesForm, ItemListaMaterialesForm, BarcodeForm,
    MiembroForm, CuotaForm
)
from .simulacion import calcular_rendimiento


def home(request):
    return render(request, 'core/home.html')


@login_required
def products(request):
    # Obtener todas las variedades asociadas al usuario actual
    variedades = Variedad.objects.filter(user=request.user)
    context = {
        'variedades': variedades,
    }
    return render(request, 'core/products.html', context)


# Vistas para Variedad
class VariedadListView(ListView):
    model = Variedad
    template_name = 'core/variedad_list.html'
    context_object_name = 'variedades'

class VariedadCreateView(CreateView):
    model = Variedad
    form_class = VariedadForm
    template_name = 'core/variedad_form.html'
    success_url = reverse_lazy('variedad_list')

class VariedadUpdateView(UpdateView):
    model = Variedad
    form_class = VariedadForm
    template_name = 'core/variedad_form.html'
    success_url = reverse_lazy('variedad_list')

class VariedadDeleteView(DeleteView):
    model = Variedad
    template_name = 'core/variedad_confirm_delete.html'
    success_url = reverse_lazy('variedad_list')


@login_required
def variedad_create(request):
    if request.method == 'POST':
        form = VariedadForm(request.POST)
        if form.is_valid():
            variedad = form.save(commit=False)
            variedad.user = request.user  # Asigna el usuario actual a la Variedad
            variedad.save()
            return redirect('products')
    else:
        form = VariedadForm()
    return render(request, 'core/variedad_form.html', {'form': form})


@login_required
def variedad_update(request, pk):
    variedad = get_object_or_404(Variedad, pk=pk)
    if request.method == 'POST':
        form = VariedadForm(request.POST, instance=variedad)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = VariedadForm(instance=variedad)
    return render(request, 'core/variedad_form.html', {'form': form})

@login_required
def variedad_delete(request, pk):
    variedad = get_object_or_404(Variedad, pk=pk)
    if request.method == 'POST':
        variedad.delete()
        return redirect('products')
    return render(request, 'core/variedad_confirm_delete.html', {'variedad': variedad})

# vista de registro / registrarse - signup
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Obtener la contraseña en texto plano
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def mi_vista(request):
    context = {
        'nombre_usuario': request.user.get_username()
    }
    return render(request, 'base.html', context)


def exit(request):
    logout(request)
    return redirect('home')

# Vistas para CondicionesCultivo
@login_required
def condiciones_cultivo_list(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    condiciones = variedad.condiciones.all()  # Access related objects using 'condiciones'
    return render(request, 'core/condiciones_cultivo_list.html', {'condiciones': condiciones, 'variedad': variedad})


@login_required
def condiciones_cultivo_create(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    if request.method == 'POST':
        form = CondicionesCultivoForm(request.POST)
        if form.is_valid():
            condicion = form.save(commit=False)
            condicion.variedad = variedad
            condicion.save()
            return redirect('condiciones_cultivo_list', variedad_id=variedad.pk)
        else:
            print("Formulario inválido") 
            print(form.errors) 
    else:
        # placeholder  para la fecha (DD/MM/YYYY)
        form = CondicionesCultivoForm(initial={'variedad': variedad})
        form.fields['registro_fecha'].widget.attrs['placeholder'] = 'DD/MM/YYYY' 
    return render(request, 'core/condiciones_cultivo_form.html', {'form': form, 'variedad': variedad})


@login_required
def condiciones_cultivo_update(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    condicion = get_object_or_404(CondicionesCultivo, pk=pk, variedad=variedad)
    if request.method == 'POST':
        form = CondicionesCultivoForm(request.POST, instance=condicion)
        if form.is_valid():
            form.save()
            return redirect('condiciones_cultivo_list', variedad_id=variedad.pk)
    else:
        form = CondicionesCultivoForm(instance=condicion)
    return render(request, 'core/condiciones_cultivo_form.html', {'form': form, 'variedad': variedad})

@login_required
def condiciones_cultivo_delete(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    condicion = get_object_or_404(CondicionesCultivo, pk=pk, variedad=variedad)
    if request.method == 'POST':
        condicion.delete()
        return redirect('condiciones_cultivo_list', variedad_id=variedad.pk)
    return render(request, 'core/condiciones_cultivo_confirm_delete.html', {'condicion': condicion, 'variedad': variedad})

# Vistas para TratamientoFitofarmaceutico
@login_required
def tratamiento_list(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    tratamientos = variedad.tratamientos_fitofarmaceuticos.all()  # Access related objects using 'tratamientos_fitofarmaceuticos'
    return render(request, 'core/tratamiento_list.html', {'tratamientos': tratamientos, 'variedad': variedad})


@login_required
def tratamiento_create(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    if request.method == 'POST':
        form = TratamientoFitofarmaceuticoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.variedad = variedad
            tratamiento.save()
            return redirect('tratamiento_list', variedad_id=variedad.pk)
    else:
        form = TratamientoFitofarmaceuticoForm(initial={'variedad': variedad})
    return render(request, 'core/tratamiento_form.html', {'form': form, 'variedad': variedad})

@login_required
def tratamiento_update(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    tratamiento = get_object_or_404(TratamientoFitofarmaceutico, pk=pk, variedad=variedad)
    if request.method == 'POST':
        form = TratamientoFitofarmaceuticoForm(request.POST, instance=tratamiento)
        if form.is_valid():
            form.save()
            return redirect('tratamiento_list', variedad_id=variedad.pk)
    else:
        form = TratamientoFitofarmaceuticoForm(instance=tratamiento)
    return render(request, 'core/tratamiento_form.html', {'form': form, 'variedad': variedad})

@login_required
def tratamiento_delete(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    tratamiento = get_object_or_404(TratamientoFitofarmaceutico, pk=pk, variedad=variedad)
    if request.method == 'POST':
        tratamiento.delete()
        return redirect('tratamiento_list', variedad_id=variedad.pk)
    return render(request, 'core/tratamiento_confirm_delete.html', {'tratamiento': tratamiento, 'variedad': variedad})

# Vistas para AnalisisCalidad
@login_required
def analisis_list(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    analisis = variedad.analisis.all()  # Access related objects using 'analisis'
    return render(request, 'core/analisis_list.html', {'analisis': analisis, 'variedad': variedad})


@login_required
def analisis_create(request, variedad_id):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    if request.method == 'POST':
        form = AnalisisCalidadForm(request.POST, user=request.user)
        if form.is_valid():
            analisis = form.save(commit=False)
            analisis.variedad = variedad
            analisis.save()
            return redirect('analisis_list', variedad_id=variedad.pk)
        else:
            print(form.errors)  # Imprimir errores del formulario en la consola
    else:
        form = AnalisisCalidadForm(initial={'variedad': variedad}, user=request.user)
    return render(request, 'core/analisis_form.html', {'form': form, 'variedad': variedad})


def analisis_detail(request, variedad_id, analisis_id):
    user = request.user  # Obtener el usuario actualmente autenticado
    variedad = get_object_or_404(Variedad, pk=variedad_id)

    # Verificar si la variedad pertenece al usuario actual
    if variedad.user != user:
        
        return render(request, 'core/error_page.html', {'error_message': 'No tiene permiso para ver esta variedad.'})

    # Obtener el análisis si pertenece a la variedad del usuario
    analisis = get_object_or_404(AnalisisCalidad, pk=analisis_id, variedad=variedad)
    
    return render(request, 'core/analisis_detail.html', {'analisis': analisis, 'variedad': variedad, 'resultado': analisis.resultado})


@login_required
def analisis_update(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    analisis = get_object_or_404(AnalisisCalidad, pk=pk, variedad=variedad)
    if request.method == 'POST':
        form = AnalisisCalidadForm(request.POST, instance=analisis, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('analisis_list', variedad_id=variedad.pk)
    else:
        form = AnalisisCalidadForm(instance=analisis, user=request.user)
    return render(request, 'core/analisis_form.html', {'form': form, 'variedad': variedad})


@login_required
def analisis_delete(request, variedad_id, pk):
    variedad = get_object_or_404(Variedad, pk=variedad_id)
    analisis = get_object_or_404(AnalisisCalidad, pk=pk, variedad=variedad)
    if request.method == 'POST':
        analisis.delete()
        return redirect('analisis_list', variedad_id=variedad.pk)
    return render(request, 'core/analisis_confirm_delete.html', {'analisis': analisis, 'variedad': variedad})

def error_page(request, error_message):
    return render(request, 'core/error_page.html', {'error_message': error_message})

def error_404(request, exception):
    return render(request, 'core/error_page.html', status=404)

def error_500(request):
    return render(request, 'core/error_page.html', status=500)


def management_view(request):
    context = {
        'title': 'Functions Panel',
        'description': 'This is the panel where you can oversee various functions.'
    }
    return render(request, 'core/features.html', context)  

# Recomendacion - Esta función maneja la inserción de datos y redirecciona a la vista de recomendaciones
@login_required
def recomendar_cultivo_view(request):
    if request.method == 'POST':
        form = CondicionesCultivoForm(request.POST)
        if form.is_valid():
            condiciones_actuales = form.save()
            tipo_suelo_descripcion = dict(form.fields['tipo_suelo'].choices).get(condiciones_actuales.tipo_suelo)
            recomendaciones, estado_cultivo = analizar_datos_y_generar_recomendaciones(condiciones_actuales)
            
            user_session_key = f'recomendaciones_{request.user.pk}'
            request.session[user_session_key] = {
                'recomendaciones': recomendaciones,
                'estado_cultivo': estado_cultivo,
                'tipo_suelo_descripcion': tipo_suelo_descripcion,
                'condiciones': {
                    'temperatura': condiciones_actuales.temperatura,
                    'humedad': condiciones_actuales.humedad,
                    'tipo_suelo': condiciones_actuales.tipo_suelo,
                    'ph_suelo': condiciones_actuales.ph_suelo,
                    'nutrientes': condiciones_actuales.nutrientes,
                    'iluminacion': condiciones_actuales.iluminacion,
                    'temperatura_suelo': condiciones_actuales.temperatura_suelo,
                    'humedad_suelo': condiciones_actuales.humedad_suelo,
                    'temperatura_ambiente': condiciones_actuales.temperatura_ambiente,
                    'humedad_ambiente': condiciones_actuales.humedad_ambiente,
                    'concentracion_co2': condiciones_actuales.concentracion_co2,
                    'ventilacion': condiciones_actuales.ventilacion,
                    'oxigeno_suelo': condiciones_actuales.oxigeno_suelo,
                    'calidad_agua_ph': condiciones_actuales.calidad_agua_ph,
                    'calidad_agua_cloro': condiciones_actuales.calidad_agua_cloro
                }
            }
            
            return redirect('recomendaciones')
        else:
            # Puedes agregar mensajes de error o validación aquí
            print(form.errors)
    else:
        form = CondicionesCultivoForm()
    
    return render(request, 'core/recomendar_cultivo.html', {'form': form})


@login_required
def recomendaciones_view(request):
    user_session_key = f'recomendaciones_{request.user.pk}'
    datos_usuario = request.session.get(user_session_key, {})
    recomendaciones = datos_usuario.get('recomendaciones', [])
    estado_cultivo = datos_usuario.get('estado_cultivo', 'desconocido')
    tipo_suelo_descripcion = datos_usuario.get('tipo_suelo_descripcion', '')
    condiciones = datos_usuario.get('condiciones', {})
    
    # Limpia la sesión después de usarla, si es necesario
    del request.session[user_session_key]

    return render(request, 'core/recomendaciones.html', {
        'recomendaciones': recomendaciones,
        'estado_cultivo': estado_cultivo,
        'tipo_suelo_descripcion': tipo_suelo_descripcion,
        'condiciones': condiciones
    })


#Esta función maneja la visualización de las recomendaciones almacenadas en la sesión del usuario
@login_required
def recomendaciones_view(request):
    user_session_key = f'recomendaciones_{request.user.pk}'
    datos_usuario = request.session.get(user_session_key, {})
    recomendaciones = datos_usuario.get('recomendaciones', [])
    tipo_suelo_descripcion = datos_usuario.get('tipo_suelo_descripcion', '')
    condiciones = datos_usuario.get('condiciones', {})
    return render(request, 'core/recomendaciones.html', {
        'recomendaciones': recomendaciones,
        'tipo_suelo_descripcion': tipo_suelo_descripcion,
        'condiciones': condiciones
    })


#Esta función contiene la lógica para analizar los datos ingresados y generar las recomendaciones correspondientes
def analizar_datos_y_generar_recomendaciones(condiciones_actuales):
    recomendaciones = []

    # Análisis de la humedad
    if condiciones_actuales.humedad < 60:
        recomendaciones.append("Aumentar la humedad relativa para favorecer el crecimiento de las plantas.")
    elif condiciones_actuales.humedad > 70:
        recomendaciones.append("Reducir la humedad relativa para evitar problemas de hongos y enfermedades.")
    else:
        recomendaciones.append("La humedad relativa es adecuada.")

    # Análisis de la temperatura
    if condiciones_actuales.temperatura < 25:
        recomendaciones.append("Elevar la temperatura durante las horas de luz.")
    elif condiciones_actuales.temperatura > 30:
        recomendaciones.append("Disminuir la temperatura durante las horas de luz.")
    else:
        recomendaciones.append("La temperatura es adecuada.")

    # Análisis del pH del suelo
    if condiciones_actuales.ph_suelo < 6.0:
        recomendaciones.append("Ajustar el pH del suelo para mantenerlo en un nivel óptimo.")
    elif condiciones_actuales.ph_suelo > 7.5:
        recomendaciones.append("Reducir el pH del suelo para mantenerlo en un nivel óptimo.")
    else:
        recomendaciones.append("El pH del suelo es adecuado.")
    
    # Análisis de nutrientes
    if condiciones_actuales.nutrientes == 'bajo':
        recomendaciones.append("Agregar fertilizantes para suplir las deficiencias nutricionales.")
    else:
        recomendaciones.append("Los niveles de nutrientes son adecuados.")

    # Análisis de iluminación
    if 5000 <= condiciones_actuales.iluminacion < 10000:
        recomendaciones.append("La iluminación actual es adecuada para plantas jóvenes y esquejes.")
    elif 10000 <= condiciones_actuales.iluminacion < 15000:
        recomendaciones.append("Aumentar la iluminación para favorecer el desarrollo en plantas jóvenes y esquejes.")
    elif 15000 <= condiciones_actuales.iluminacion < 50000:
        recomendaciones.append("La iluminación actual es adecuada para la fase de crecimiento de las plantas.")
    elif 50000 <= condiciones_actuales.iluminacion < 75000:
        recomendaciones.append("La iluminación actual es adecuada para la fase de floración de las plantas.")
    elif condiciones_actuales.iluminacion >= 75000:
        recomendaciones.append("Reducir la iluminación para evitar posibles daños por exceso de luz.")
    else:
        recomendaciones.append("La iluminación es adecuada.")

    # Análisis de temperatura del suelo
    if condiciones_actuales.temperatura_suelo < 15:
        recomendaciones.append("Aumentar la temperatura del suelo para un crecimiento óptimo.")
    elif condiciones_actuales.temperatura_suelo > 25:
        recomendaciones.append("Disminuir la temperatura del suelo para evitar el estrés térmico.")
    else:
        recomendaciones.append("La temperatura del suelo es adecuada.")

    # Análisis de humedad del suelo
    if condiciones_actuales.humedad_suelo < 50:
        recomendaciones.append("Aumentar la humedad del suelo para mejorar la disponibilidad de agua.")
    elif condiciones_actuales.humedad_suelo > 70:
        recomendaciones.append("Reducir la humedad del suelo para evitar problemas de pudrición de raíces.")
    else:
        recomendaciones.append("La humedad del suelo es adecuada.")

    # Análisis de CO2
    if condiciones_actuales.concentracion_co2 < 400:
        recomendaciones.append("Aumentar la concentración de CO2 para mejorar la fotosíntesis.")
    else:
        recomendaciones.append("La concentración de CO2 es adecuada.")
    
    # Análisis de oxígeno en el suelo
    if condiciones_actuales.oxigeno_suelo < 10:
        recomendaciones.append("Mejorar la aireación del suelo para aumentar la concentración de oxígeno.")
    else:
        recomendaciones.append("La concentración de oxígeno en el suelo es adecuada.")

    # Análisis de calidad del agua
    if condiciones_actuales.calidad_agua_ph < 6:
        recomendaciones.append("Ajustar el pH del agua de riego.")
    if condiciones_actuales.calidad_agua_cloro > 0:
        recomendaciones.append("Reducir las concentraciones de cloro en el agua de riego.")
    else:
        recomendaciones.append("La calidad del agua es adecuada.")

    # Si no hay recomendaciones específicas, agregar un mensaje general
    if not recomendaciones:
        recomendaciones.append("Las condiciones actuales son óptimas. Continuar con el cuidado actual.")

    estado_cultivo = "óptimo" if recomendaciones == ["Las condiciones actuales son óptimas. Continuar con el cuidado actual."] else "subóptimo"
    return recomendaciones, estado_cultivo


@login_required
def todas_condiciones_cultivo(request):
    variedades = Variedad.objects.filter(user=request.user)
    condiciones = CondicionesCultivo.objects.filter(variedad__in=variedades)
    
    return render(request, 'core/condiciones_cultivo.html', {'condiciones': condiciones})

#--- PDF --------- 
@login_required
def generar_pdf_recomendaciones(request):
    user_session_key = f'recomendaciones_{request.user.pk}'
    datos_usuario = request.session.get(user_session_key, {})
    recomendaciones = datos_usuario.get('recomendaciones', [])
    condiciones = datos_usuario.get('condiciones', {})
    tipo_suelo_descripcion = datos_usuario.get('tipo_suelo_descripcion', '')
    estado_cultivo = datos_usuario.get('estado_cultivo', '')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recomendaciones.pdf"'

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Agregar contenido al PDF
    contenido = []

    # Cabecera
    cabecera = Paragraph("Recomendaciones de Cultivo", styles['Heading1'])
    contenido.append(cabecera)
    contenido.append(Spacer(1, 12))

    # Datos Ingresados
    contenido.append(Paragraph("Datos Ingresados:", styles['Heading2']))
    contenido.append(Spacer(1, 6))
    contenido.append(Paragraph(f"Temperatura: {condiciones.get('temperatura')} °C", styles['Normal']))
    contenido.append(Paragraph(f"Humedad: {condiciones.get('humedad')} %", styles['Normal']))
    contenido.append(Paragraph(f"Tipo de Suelo: {condiciones.get('tipo_suelo')} ({tipo_suelo_descripcion})", styles['Normal']))
    contenido.append(Paragraph(f"pH del Suelo: {condiciones.get('ph_suelo')}", styles['Normal']))
    contenido.append(Paragraph(f"Nutrientes: {condiciones.get('nutrientes')}", styles['Normal']))
    contenido.append(Paragraph(f"Iluminación: {condiciones.get('iluminacion')} lux", styles['Normal']))
    contenido.append(Paragraph(f"Temperatura del Suelo: {condiciones.get('temperatura_suelo')} °C", styles['Normal']))
    contenido.append(Paragraph(f"Humedad del Suelo: {condiciones.get('humedad_suelo')} %", styles['Normal']))
    contenido.append(Paragraph(f"Temperatura Ambiente: {condiciones.get('temperatura_ambiente')} °C", styles['Normal']))
    contenido.append(Paragraph(f"Humedad Ambiente: {condiciones.get('humedad_ambiente')} %", styles['Normal']))
    contenido.append(Paragraph(f"Concentración de CO2: {condiciones.get('concentracion_co2')} ppm", styles['Normal']))
    contenido.append(Paragraph(f"Ventilación: {condiciones.get('ventilacion')}", styles['Normal']))
    contenido.append(Paragraph(f"Oxígeno en el Suelo: {condiciones.get('oxigeno_suelo')} %", styles['Normal']))
    contenido.append(Paragraph(f"Calidad del Agua (pH): {condiciones.get('calidad_agua_ph')}", styles['Normal']))
    contenido.append(Paragraph(f"Calidad del Agua (Cloro): {condiciones.get('calidad_agua_cloro')} ppm", styles['Normal']))
    contenido.append(Spacer(1, 12))

    # Recomendaciones
    contenido.append(Paragraph(" CannaTech - Recomendaciones de Cultivo:", styles['Heading2']))
    contenido.append(Spacer(1, 6))
    for recomendacion in recomendaciones:
        contenido.append(Paragraph(recomendacion, styles['Normal']))
    contenido.append(Spacer(1, 12))

    # Descripción del Tipo de Suelo
    contenido.append(Paragraph("Descripción del Tipo de Suelo:", styles['Heading2']))
    contenido.append(Spacer(1, 6))
    contenido.append(Paragraph(tipo_suelo_descripcion, styles['Normal']))
    contenido.append(Spacer(1, 12))

    # Estado del Cultivo
    contenido.append(Paragraph("Estado del Cultivo:", styles['Heading2']))
    contenido.append(Spacer(1, 6))
    contenido.append(Paragraph(estado_cultivo, styles['Normal']))
    contenido.append(Spacer(1, 12))

    pdf.build(contenido)
    
    response.write(buffer.getvalue())
    buffer.close()
    return response


def home_view_facts(request):
    management_view_url = reverse('management-view')
    context = {
        'management_view_url': management_view_url,
        # otros contextos aquí
    }
    return render(request, 'core/home.html', context)


def condiciones_cultivo_view(request):
    condiciones = CondicionesCultivo.objects.all().order_by('variedad__nombre', 'registro_fecha')
    return render(request, 'core/home.html', {'condiciones': condiciones})


def home_datos_usuario(request):
    if request.user.is_authenticated:
        # Obtener todas las variedades asociadas al usuario actual
        variedades = Variedad.objects.filter(user=request.user)
        # Obtener más datos relacionados con el usuario
        context = {
            'variedades': variedades,
            # Agregar otros contextos según lo que se necesites mostrar...
        }
        return render(request, 'core/home.html', context)
    else:
        return render(request, 'core/home.html')


# simulacion rendimentos funcion
@login_required
def simular_rendimiento(request):
    if request.method == 'POST':
        form = CultivoForm(request.POST)
        if form.is_valid():
            cultivo = form.save()
            rendimiento = calcular_rendimiento(cultivo)
            return render(request, 'core/resultado.html', {'rendimiento': rendimiento, 'cultivo': cultivo})
    else:
        form = CultivoForm()
    return render(request, 'core/simulacion.html', {'form': form})

@login_required
def analizar_costos_presupuestos(request):
    form = AnalisisCostosForm(request.POST or None)
    if form.is_valid():
        analisis = form.save(commit=False)
        analisis.costo_total = (
            analisis.costo_semilla + analisis.costo_sustrato +
            analisis.costo_energia + analisis.costo_agua +
            analisis.costo_manobra
        )
        analisis.diferencia = analisis.presupuesto - analisis.costo_total
        analisis.costo_por_gramo = analisis.costo_total / analisis.produccion_gramos if analisis.produccion_gramos else None
        analisis.save()
        return render(request, 'core/resultados_analisis_costos_presupuestos.html', {'resultados': analisis})
    return render(request, 'core/formulario_costos_presupuestos.html', {'form': form})


# Vista para mostrar la lista de clientes
@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/clientes.html', {'clientes': clientes})

# Vista para crear un nuevo cliente
@login_required
def cliente_nuevo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('clientes')
    else:
        form = ClienteForm()
    return render(request, 'core/cliente_nuevo.html', {'form': form})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/cliente_editar.html', {'form': form})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        nombre_cliente = cliente.nombre
        cliente.delete()
        messages.success(request, f'Cliente "{nombre_cliente}" eliminado exitosamente.')
        return redirect('clientes')
    return redirect('clientes')

@login_required
def recepcion_muestra(request):
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            tipo_texto = form.cleaned_data.get('tipo')
            if tipo_texto:
                tipo_analisis, created = TipoAnalisis.objects.get_or_create(nombre=tipo_texto)
            else:
                tipo_analisis = None
            muestra = form.save(commit=False)
            muestra.tipo_analisis = tipo_analisis
            muestra.save()
            messages.success(request, f'Muestra {muestra.codigo} registrada exitosamente.')
            return redirect('programar_analisis', muestra.id)
    else:
        form = MuestraForm()
    return render(request, 'core/recepcion_muestra.html', {'form': form})


@login_required
def programar_analisis(request, muestra_id=None):
    muestras_pendientes = Muestra.objects.filter(analisisprogramado__isnull=True)
    if request.method == 'POST':
        form = AnalisisProgramadoForm(request.POST)
        if form.is_valid():
            # Guarda el análisis programado asociado a la muestra_id
            analisis_programado = form.save(commit=False)
            if muestra_id is not None:
                analisis_programado.muestra_id = muestra_id
            analisis_programado.save()
            
            messages.success(request, f'Análisis {analisis_programado.tipo_analisis} programado para la muestra {analisis_programado.muestra.codigo}.')
            return redirect('registro_resultados')
    else:
        form = AnalisisProgramadoForm()
    
    # Pasa muestra_id al contexto del renderizado
    return render(request, 'core/programar_analisis.html', {'form': form, 'muestras_pendientes': muestras_pendientes, 'muestra_id': muestra_id})

@login_required
def registro_resultados(request):
    analisis_pendientes = AnalisisProgramado.objects.filter(resultadoanalisis__isnull=True)
    if request.method == 'POST':
        form = ResultadoAnalisisForm(request.POST)
        if form.is_valid():
            try:
                resultado_analisis = form.save(commit=False)
                
                # Convertir la fecha a una fecha consciente de la zona horaria 
                fecha_analisis = resultado_analisis.fecha_analisis
                if timezone.is_naive(fecha_analisis):
                    fecha_analisis = timezone.make_aware(fecha_analisis, timezone=timezone.get_current_timezone())
                resultado_analisis.fecha_analisis = fecha_analisis

                resultado_analisis.save()
                messages.success(request, f'Resultados registrados para el análisis {resultado_analisis.analisis_programado.tipo_analisis} de la muestra {resultado_analisis.analisis_programado.muestra.codigo}.')
                return redirect('ver_informes')
            except Exception as e:
                messages.error(request, f'Error al registrar los resultados: {e}')
        else:
            messages.error(request, 'Hubo un error en la validación del formulario. Verifique los datos ingresados.')
    else:
        form = ResultadoAnalisisForm()
    
    return render(request, 'core/registro_resultados.html', {'form': form, 'analisis_pendientes': analisis_pendientes})

@login_required
def ver_informes(request):
    resultados = ResultadoAnalisis.objects.all()

    # Obtener el conteo de análisis por tipo de análisis
    analisis_por_tipo = resultados.values('analisis_programado__tipo_analisis__nombre').annotate(conteo=Count('id'))

    # Preparar los datos para el informe
    informe_datos = {
        'total_analisis': resultados.count(),
        'analisis_por_tipo': analisis_por_tipo
    }

    return render(request, 'core/ver_informes.html', {'informe_datos': informe_datos})

def barcodes_view(request):
    # vista seleccion de codigo de barra para generar
    return render(request, 'core/barcodes.html')

# Bar code

@login_required
def barcode_form(request):
    if request.method == 'POST':
        form = BarcodeForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product_code = form.cleaned_data['product_code']
            is_favorite = form.cleaned_data.get('is_favorite', False)
            barcode_type = 'code128'

            # Crear o actualizar el producto
            product, created = Product.objects.get_or_create(
                code=product_code,
                defaults={'name': product_name, 'user': request.user}
            )
            product.is_favorite = is_favorite
            product.save()

            # Generar código de barras y guardarlo en un BytesIO
            buffer = BytesIO()
            BarcodeClass = barcode.get_barcode_class(barcode_type)
            barcode_instance = BarcodeClass(product_code, writer=ImageWriter())
            barcode_instance.write(buffer)
            buffer.seek(0)

            # Convertir la imagen a un objeto PIL
            barcode_image = Image.open(buffer)

            # Crear una nueva imagen con espacio para el texto
            width, height = barcode_image.size
            font_size = 20  
            total_height = height + font_size + 10
            new_image = Image.new('RGB', (width, total_height), 'white')
            draw = ImageDraw.Draw(new_image)

            # Cargar la fuente TrueType
            try:
                font_path = os.path.join('fonts', 'arial.ttf')  
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                font = ImageFont.load_default()

            # Añadir el nombre del producto arriba del código de barras
            text_width = draw.textlength(product_name, font=font)
            text_x = (width - text_width) / 2
            draw.text((text_x, 10), product_name, fill="black", font=font)

            # Pegar el código de barras en la nueva imagen
            new_image.paste(barcode_image, (0, font_size + 10))

            # Convertir la imagen a base64
            buffer = BytesIO()
            new_image.save(buffer, format='PNG')
            buffer.seek(0)
            barcode_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

            context = {
                'product': product,
                'barcode_img': barcode_img,
            }
            return render(request, 'core/barcode_result.html', context)
    else:
        form = BarcodeForm()
    return render(request, 'core/barcode_form.html', {'form': form})

@login_required
def barcode_form2(request):
    if request.method == 'POST':
        form = BarcodeForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            product_code = form.cleaned_data['product_code']
            is_favorite = form.cleaned_data.get('is_favorite', False)
            barcode_type = 'code128'

            # Crear o actualizar el producto
            product, created = Product.objects.get_or_create(
                code=product_code,
                defaults={'name': product_name, 'user': request.user}
            )
            product.is_favorite = is_favorite
            product.save()

            # Combinar datos en un solo string delimitado por "|"
            barcode_data = f"{product_name}|{product_code}"

            # Generar código de barras
            BarcodeClass = barcode.get_barcode_class(barcode_type)
            barcode_instance = BarcodeClass(barcode_data, writer=ImageWriter())
            barcode_image = barcode_instance.render()

            # Crear una nueva imagen vacía para combinar el código de barras y el código del producto
            combined_image = Image.new('RGB', (barcode_image.width, barcode_image.height + 30), (255, 255, 255))
            combined_image.paste(barcode_image, (0, 0))

            # Agregar solo el código del producto debajo del código de barras
            draw = ImageDraw.Draw(combined_image)
            font = ImageFont.load_default()
            text_width, text_height = draw.textbbox((0, 0), product_code, font=font)[2:]
            draw.text(((combined_image.width - text_width) / 2, barcode_image.height), product_code, font=font, fill=(0, 0, 0))

            # Convertir la imagen combinada a base64
            buffer = BytesIO()
            combined_image.save(buffer, format='PNG')
            barcode_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

            context = {
                'product': product,
                'barcode_img': barcode_img,
            }
            return render(request, 'core/barcode_result2.html', context)
    else:
        form = BarcodeForm()
    return render(request, 'core/barcode_form2.html', {'form': form})

@login_required
def decode_barcode_view(request):
    if request.method == 'GET':
        barcode_img = request.GET.get('barcode_img')
        if barcode_img:
            product_name, product_code = decode_barcode(barcode_img)
            context = {
                'product_name': product_name,
                'product_code': product_code,
            }
            return render(request, 'core/barcode_decoded.html', context)
        else:
            return HttpResponseBadRequest('No se proporcionó una imagen de código de barras')
    else:
        return HttpResponseBadRequest('Método no permitido')
    

@login_required
def favorite_barcodes(request):
    favorites = Product.objects.filter(user=request.user, is_favorite=True)
    return render(request, 'core/favorite_barcodes.html', {'favorites': favorites})

def decode_barcode(barcode_data):
    barcode_format = barcode.get_barcode_class('code128')
    barcode_object = barcode_format(barcode_data)
    decoded_data = barcode_object.get_fullcode()
    product_name, product_code = decoded_data.split('|')
    return product_name, product_code


@login_required
# Barra de Busqueda
def search_results(request):
    query = request.GET.get('q')
    results = {}

    if query:
        variedades = Variedad.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
        results['variedades'] = variedades

        tipos_analisis = TipoAnalisis.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(metodo__icontains=query)
        )
        results['tipos_analisis'] = tipos_analisis

        condiciones_cultivo = CondicionesCultivo.objects.filter(
            Q(variedad__nombre__icontains=query) | Q(tipo_suelo__icontains=query)
        )
        results['condiciones_cultivo'] = condiciones_cultivo

        cultivos = Cultivo.objects.filter(
            Q(variedad__nombre__icontains=query) | Q(cantidad_plantas__icontains=query)
        )
        results['cultivos'] = cultivos

        analisis_costos = AnalisisCostos.objects.filter(
            Q(id__icontains=query) | Q(costo_semilla__icontains=query)
        )
        results['analisis_costos'] = analisis_costos

        tratamientos_fitofarmaceuticos = TratamientoFitofarmaceutico.objects.filter(
            Q(variedad__nombre__icontains=query) | Q(tratamiento__icontains=query)
        )
        results['tratamientos_fitofarmaceuticos'] = tratamientos_fitofarmaceuticos

        analisis_calidad = AnalisisCalidad.objects.filter(
            Q(variedad__nombre__icontains=query) | Q(tipo_analisis__icontains=query) | Q(resultado__icontains=query)
        )
        results['analisis_calidad'] = analisis_calidad

        clientes = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(direccion__icontains=query) | Q(telefono__icontains=query) | Q(email__icontains=query)
        )
        results['clientes'] = clientes

        muestras = Muestra.objects.filter(
            Q(codigo__icontains=query) | Q(cliente__nombre__icontains=query)
        )
        results['muestras'] = muestras

        analisis_programados = AnalisisProgramado.objects.filter(
            Q(tipo_analisis__nombre__icontains=query) | Q(prioridad__icontains=query)
        )
        results['analisis_programados'] = analisis_programados

        resultados_analisis = ResultadoAnalisis.objects.filter(
            Q(analisis_programado__tipo_analisis__nombre__icontains=query) | Q(observaciones__icontains=query)
        )
        results['resultados_analisis'] = resultados_analisis

        productos = Product.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        )
        results['productos'] = productos

        gastos_operativos = GastoOperativo.objects.filter(
            Q(tipo_gasto__icontains=query) | Q(descripcion__icontains=query) |
            Q(variedad__nombre__icontains=query)
        )
        results['gastos_operativos'] = gastos_operativos

        # Añadir búsqueda para Venta
        ventas = Venta.objects.filter(
            Q(producto__icontains=query) | Q(variedad__nombre__icontains=query)
        )
        results['ventas'] = ventas

        # Añadir búsqueda para Pedido
        pedidos = Pedido.objects.filter(
            Q(producto__icontains=query) | Q(variedad__nombre__icontains=query)
        )
        results['pedidos'] = pedidos        
    
        
        materiales = Material.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
        results['materiales'] = materiales

        listas_materiales = ListaMateriales.objects.filter(
            Q(nombre_producto__icontains=query)
        )
        results['listas_materiales'] = listas_materiales

        items_listas_materiales = ItemListaMateriales.objects.filter(
            Q(material__nombre__icontains=query) | Q(lista_materiales__nombre_producto__icontains=query)
        )
        results['items_listas_materiales'] = items_listas_materiales

        planes_produccion = PlanProduccion.objects.filter(
            Q(nombre__icontains=query) | Q(detalles__icontains=query)
        )
        results['planes_produccion'] = planes_produccion

        tareas_produccion = TareaProduccion.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query) | Q(asignado_a__icontains=query)
        )
        results['tareas_produccion'] = tareas_produccion

        miembros = Miembro.objects.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(email__icontains=query) | Q(numero_socio__icontains=query)
        )
        results['miembros'] = miembros

        cuotas = Cuota.objects.filter(
            Q(miembro__nombre__icontains=query) | Q(miembro__apellido__icontains=query)
        )
        results['cuotas'] = cuotas

        return render(request, 'core/search_results.html', {'query': query, 'results': results})


# graficos 
from rest_framework import viewsets
from .serializers import CondicionesCultivoSerializer

class CondicionesCultivoViewSet(viewsets.ModelViewSet):
    queryset = CondicionesCultivo.objects.all()
    serializer_class = CondicionesCultivoSerializer
    
def visualizacion_graficos(request):
    condiciones = CondicionesCultivo.objects.all()  # Obtener datos para los gráficos
    context = {'condiciones': condiciones}
    return render(request, 'core/visualizacion.html', context)


#vista para dashboard cards
@login_required
def dashboard(request):
    gasto_form = GastoOperativoForm()
    venta_form = VentaForm()
    pedido_form = PedidoForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'gasto_form':
            gasto_form = GastoOperativoForm(request.POST)
            if gasto_form.is_valid():
                gasto_form.save()
                messages.success(request, 'Gasto guardado correctamente.')
                return redirect('dashboard')
            else:
                messages.error(request, f'Error en el formulario de gasto: {gasto_form.errors}')
        elif form_type == 'venta_form':
            venta_form = VentaForm(request.POST)
            if venta_form.is_valid():
                venta_form.save()
                messages.success(request, 'Venta guardada correctamente.')
                return redirect('dashboard')
            else:
                messages.error(request, f'Error en el formulario de venta: {venta_form.errors}')
        elif form_type == 'pedido_form':
            pedido_form = PedidoForm(request.POST)
            if pedido_form.is_valid():
                pedido_form.save()
                messages.success(request, 'Pedido guardado correctamente.')
                return redirect('dashboard')
            else:
                messages.error(request, f'Error en el formulario de pedido: {pedido_form.errors}')

    context = {
        'gasto_form': gasto_form,
        'venta_form': venta_form,
        'pedido_form': pedido_form,
        'gastos': GastoOperativo.objects.all(),  
        'ventas': Venta.objects.all(),  
        'pedidos': Pedido.objects.all(),
        'variedades': Variedad.objects.all(),
    }
    return render(request, 'core/dashboard.html', context)

def borrar_gasto(request, gasto_id):
    gasto = get_object_or_404(GastoOperativo, id=gasto_id)
    if request.method == 'POST':
        gasto.delete()
        messages.success(request, 'Gasto eliminado correctamente.')
    return redirect('dashboard')

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada correctamente.')
    return redirect('dashboard')

def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado correctamente.')
    return redirect('dashboard')


# graficar dashboard info 
from django.db.models import Sum, F
import matplotlib.pyplot as plt
import urllib.parse

@login_required
def graficar_datos(request):
    # Obtener datos para los gráficos
    gastos = GastoOperativo.objects.all()
    ventas = Venta.objects.all()
    pedidos = Pedido.objects.all()

    # Lógica para procesar los datos y prepararlos para los gráficos
    total_gastos = GastoOperativo.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    total_ventas = Venta.objects.aggregate(total=Sum(F('cantidad') * F('precio_unitario')))['total'] or 0
    total_pedidos = Pedido.objects.count()

    # Crear gráfico de barras
    fig, ax = plt.subplots()
    labels = ['Gastos', 'Ventas']
    valores = [total_gastos, total_ventas]
    ax.bar(labels, valores)
    ax.set_ylabel('Monto')
    ax.set_title('Resumen Financiero')
    plt.xticks(rotation=45)
    
    # Guardar el gráfico en un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen a base64 para mostrarla en la plantilla HTML
    imagen_png_base64 = urllib.parse.quote(base64.b64encode(imagen_png).decode())

    context = {
        'gastos': gastos,
        'ventas': ventas,
        'pedidos': pedidos,
        'total_gastos': total_gastos,
        'total_ventas': total_ventas,
        'total_pedidos': total_pedidos,
        'imagen_png_base64': imagen_png_base64,
    }
    return render(request, 'core/graficos_dashboard.html', context)


#BOM
def lista_planes_produccion(request):
    planes = PlanProduccion.objects.all()
    return render(request, 'core/lista_planes_produccion.html', {'planes': planes})

def detalle_plan_produccion(request, pk):
    plan = get_object_or_404(PlanProduccion, pk=pk)
    tareas = plan.tareaproduccion_set.all()
    return render(request, 'core/detalle_plan_produccion.html', {'plan': plan, 'tareas': tareas})

def crear_plan_produccion(request):
    if request.method == 'POST':
        form = PlanProduccionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_planes_produccion')
    else:
        form = PlanProduccionForm()
    return render(request, 'core/formulario_plan_produccion.html', {'form': form})


def eliminar_plan_produccion(request, pk):
    plan = get_object_or_404(PlanProduccion, pk=pk)
    plan.delete()
    return redirect('lista_planes_produccion')

def lista_bom(request):
    listas = ListaMateriales.objects.all()
    return render(request, 'core/lista_bom.html', {'listas': listas})

def detalle_bom(request, pk):
    lista = get_object_or_404(ListaMateriales, pk=pk)
    items = lista.itemlistamateriales_set.all()
    return render(request, 'core/detalle_bom.html', {'lista': lista, 'items': items})

def crear_bom(request):
    if request.method == 'POST':
        form = ListaMaterialesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_bom')
    else:
        form = ListaMaterialesForm()
    
    print("Campos del formulario:", form.fields.keys())
    return render(request, 'core/formulario_bom.html', {'form': form})


def lista_bom(request):
    listas = ListaMateriales.objects.all()
    return render(request, 'core/lista_bom.html', {'listas': listas})

def eliminar_bom(request, pk):
    bom = get_object_or_404(ListaMateriales, pk=pk)
    if request.method == 'POST':
        bom.delete()
        return redirect('lista_bom')
    return redirect('lista_bom')

def panel_de_control(request):
    return render(request, 'core/panel.html')


# Gestión de Membresías Miembros y Cuotas
@login_required
def registrar_miembro(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save()
            messages.success(request, f'Miembro {miembro.nombre_completo()} registrado exitosamente.')
            return redirect('lista_miembros')
    else:
        form = MiembroForm()
    return render(request, 'core/registrar_miembro.html', {'form': form})


@login_required
def lista_miembros(request):
    miembros = Miembro.objects.all().order_by('numero_socio')
    return render(request, 'core/admin_miembros.html', {'miembros': miembros})


@login_required
def detalle_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    cuotas = Cuota.objects.filter(miembro=miembro).order_by('-fecha_pago')
    
    if request.method == 'POST':
        form = CuotaForm(request.POST)
        if form.is_valid():
            cuota = form.save(commit=False)
            cuota.miembro = miembro
            cuota.save()
            messages.success(request, 'Cuota registrada exitosamente.')
            return redirect('detalle_miembro', miembro_id=miembro.id)
    else:
        form = CuotaForm(initial={'fecha_pago': timezone.now().date()})
    
    return render(request, 'core/detalle_miembro.html', {
        'miembro': miembro, 
        'cuotas': cuotas, 
        'form': form
    })



@login_required
def historial_cuotas_todos_miembros(request):
    # Obtener todos los miembros
    miembros = Miembro.objects.all()

    # Crear una lista para almacenar todas las cuotas de todos los miembros
    todas_las_cuotas = []

    # Iterar sobre cada miembro y obtener sus cuotas
    for miembro in miembros:
        cuotas_miembro = Cuota.objects.filter(miembro=miembro).order_by('-fecha_pago')
        todas_las_cuotas.append({
            'miembro': miembro,
            'cuotas': cuotas_miembro,
        })

    return render(request, 'core/historial_cuotas_todos_miembros.html', {'todas_las_cuotas': todas_las_cuotas})

    
@login_required
def reporte_cuotas(request):
    cuotas_pendientes = Cuota.objects.filter(pagado=False).order_by('fecha_pago')
    return render(request, 'core/reporte_cuotas.html', {'cuotas_pendientes': cuotas_pendientes})

@login_required
def editar_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    if request.method == 'POST':
        form = MiembroForm(request.POST, instance=miembro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información del miembro actualizada exitosamente.')
            return redirect('detalle_miembro', miembro_id=miembro.id)
    else:
        form = MiembroForm(instance=miembro)
    return render(request, 'core/editar_miembro.html', {'form': form, 'miembro': miembro})


@login_required
def eliminar_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    if request.method == 'POST':
        nombre_miembro = f"{miembro.nombre} {miembro.apellido}"
        miembro.delete()
        messages.success(request, f'Miembro "{nombre_miembro}" eliminado exitosamente.')
        return redirect('lista_miembros')
    return redirect('lista_miembros')


# cuotas 
def historial_pagos(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    cuotas = Cuota.objects.filter(miembro=miembro)
    context = {
        'miembro': miembro,
        'cuotas': cuotas,
    }
    return render(request, 'core/historial_pagos.html', context)

def eliminar_cuota(request, cuota_id):
    cuota = get_object_or_404(Cuota, id=cuota_id)
    if request.method == 'POST':
        cuota.delete()
        messages.success(request, 'La cuota ha sido eliminada correctamente.')
    return redirect('historial_pagos', miembro_id=cuota.miembro.id)

def eliminar_todas_cuotas(request, miembro_id):
    if request.method == 'POST':
        miembro = get_object_or_404(Miembro, id=miembro_id)
        Cuota.objects.filter(miembro=miembro).delete()
        messages.success(request, 'Todas las cuotas han sido eliminadas.')
    return redirect('detalle_miembro', miembro_id=miembro_id)


def marcar_pagado(request, cuota_id):
    cuota = get_object_or_404(Cuota, id=cuota_id)
    cuota.pagado = True
    cuota.save()
    messages.success(request, 'La cuota ha sido marcada como pagada.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def historial_pagos(request, miembro_id):
    pagos = Pago.objects.filter(miembro_id=miembro_id)
    return render(request, 'core/historial_pagos.html', {'pagos': pagos})


#CSV database plants
def plant_list(request):
    query = request.GET.get('q')
    if query:
        plants = CannabisPlant.objects.filter(strain__icontains=query)
    else:
        plants = CannabisPlant.objects.all()

    paginator = Paginator(plants, 6)  # 6 plantas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/plant_list.html', {'page_obj': page_obj, 'query': query})

