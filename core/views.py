from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse
from .forms import RegisterForm, VariedadForm, CondicionesCultivoForm, TratamientoFitofarmaceuticoForm, AnalisisCalidadForm
from .models import Variedad, CondicionesCultivo, TratamientoFitofarmaceutico, AnalisisCalidad, Variedad
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from io import BytesIO
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from .forms import CultivoForm
from .simulacion import calcular_rendimiento
from .forms import AnalisisCostosForm
from .models import Cliente, Muestra, AnalisisProgramado, ResultadoAnalisis
from .forms import ClienteForm, MuestraForm, AnalisisProgramadoForm, ResultadoAnalisisForm
from django.db.models import Count
from django.contrib import messages




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


#Analisis

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/clientes.html', {'clientes': clientes})

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

def recepcion_muestra(request):
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            muestra = form.save()
            messages.success(request, f'Muestra {muestra.codigo} registrada exitosamente.')
            return redirect('programar_analisis')
    else:
        form = MuestraForm()
    return render(request, 'core/recepcion_muestra.html', {'form': form})

def programar_analisis(request):
    muestras_pendientes = Muestra.objects.filter(analisisprogramado__isnull=True)
    if request.method == 'POST':
        form = AnalisisProgramadoForm(request.POST)
        if form.is_valid():
            analisis_programado = form.save()
            messages.success(request, f'Análisis {analisis_programado.tipo_analisis} programado para la muestra {analisis_programado.muestra.codigo}.')
            return redirect('registro_resultados')
    else:
        form = AnalisisProgramadoForm()
    return render(request, 'core/programar_analisis.html', {'form': form, 'muestras_pendientes': muestras_pendientes})

def registro_resultados(request):
    analisis_pendientes = AnalisisProgramado.objects.filter(resultadoanalisis__isnull=True)
    if request.method == 'POST':
        form = ResultadoAnalisisForm(request.POST)
        if form.is_valid():
            resultado_analisis = form.save()
            messages.success(request, f'Resultados registrados para el análisis {resultado_analisis.analisis_programado.tipo_analisis} de la muestra {resultado_analisis.analisis_programado.muestra.codigo}.')
            return redirect('ver_informes')
    else:
        form = ResultadoAnalisisForm()
    return render(request, 'core/registro_resultados.html', {'form': form, 'analisis_pendientes': analisis_pendientes})


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