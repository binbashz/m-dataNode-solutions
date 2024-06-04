from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import RegisterForm, VariedadForm, CondicionesCultivoForm, TratamientoFitofarmaceuticoForm, AnalisisCalidadForm
from .models import Variedad, CondicionesCultivo, TratamientoFitofarmaceutico, AnalisisCalidad, Variedad
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, HttpResponseServerError



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

# vista de registro / registarse
def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Aquí se hace el hasheo de la contraseña
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
            print("Formulario válido") 
            condicion = form.save(commit=False)
            condicion.variedad = variedad
            condicion.save()
            return redirect('condiciones_cultivo_list', variedad_id=variedad.pk)
        else:
            print("Formulario inválido") 
            print(form.errors) 
    else:
        form = CondicionesCultivoForm(initial={'variedad': variedad})
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
        # Aquí puedes manejar la situación donde el usuario no tiene permiso para ver esta variedad
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