from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from .models import Variedad, CondicionesCultivo, TratamientoFitofarmaceutico, AnalisisCalidad


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    fullname = forms.CharField(label="Nombre completo")

    class Meta:
        model = User
        fields = ("username", "fullname", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        full_name = self.cleaned_data["fullname"].split()
        if len(full_name) > 1:
            user.first_name = full_name[0]
            user.last_name = " ".join(full_name[1:])
        else:
            user.first_name = full_name[0]
            user.last_name = ""
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class VariedadForm(forms.ModelForm):
    class Meta:
        model = Variedad
        fields = ['nombre', 'descripcion']



class CondicionesCultivoForm(forms.ModelForm):
    TIPO_SUELO_CHOICES = (
        ('arcilloso', 'Arcilloso: Alta proporción de arcilla, retiene agua y nutrientes.'),
        ('arenoso', 'Arenoso: Mucha arena, muy permeable, retiene menos agua y nutrientes.'),
        ('limoso', 'Limoso: Textura suave, retiene agua y nutrientes.'),
        ('humifero', 'Humífero: Rico en materia orgánica y nutrientes, muy fértil.'),
        ('calcareo', 'Calcáreo: Alto contenido de calcio, afecta el pH del suelo.'),
        ('salino', 'Salino: Concentraciones altas de sales solubles, perjudicial para cultivos.'),
        ('turba', 'Turba: Suelo orgánico de descomposición vegetal.'),
    )

    # Define el campo tipo_suelo como ChoiceField y el campo registro_fecha como DateField
    tipo_suelo = forms.ChoiceField(
        choices=TIPO_SUELO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control tipo-suelo-select'})
    )
    registro_fecha = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'placeholder': 'DD/MM/YYYY',
            'class': 'form-control'
        })
    )

    class Meta:
        model = CondicionesCultivo
        fields = [
            'variedad', 'registro_fecha', 'temperatura', 'humedad', 'tipo_suelo', 'ph_suelo', 'nutrientes',
            'iluminacion', 'temperatura_suelo', 'humedad_suelo', 'temperatura_ambiente', 'humedad_ambiente',
            'concentracion_co2', 'ventilacion', 'oxigeno_suelo', 'calidad_agua_ph', 'calidad_agua_cloro'
        ]
        widgets = {
            'registro_fecha': forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY', 'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control'}),
            'humedad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ph_suelo': forms.NumberInput(attrs={'class': 'form-control'}),
            'nutrientes': forms.TextInput(attrs={'class': 'form-control'}),
            'iluminacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura_suelo': forms.NumberInput(attrs={'class': 'form-control'}),
            'humedad_suelo': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperatura_ambiente': forms.NumberInput(attrs={'class': 'form-control'}),
            'humedad_ambiente': forms.NumberInput(attrs={'class': 'form-control'}),
            'concentracion_co2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ventilacion': forms.TextInput(attrs={'class': 'form-control'}),
            'oxigeno_suelo': forms.NumberInput(attrs={'class': 'form-control'}),
            'calidad_agua_ph': forms.NumberInput(attrs={'class': 'form-control'}),
            'calidad_agua_cloro': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class TratamientoFitofarmaceuticoForm(forms.ModelForm):
    class Meta:
        model = TratamientoFitofarmaceutico
        fields = ['variedad', 'tratamiento', 'fecha_aplicacion', 'dosis']
        

class AnalisisCalidadForm(forms.ModelForm):
    class Meta:
        model = AnalisisCalidad
        fields = ['variedad', 'tipo_analisis', 'resultado', 'fecha_analisis']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AnalisisCalidadForm, self).__init__(*args, **kwargs)
        self.fields['variedad'].queryset = Variedad.objects.filter(user=user)
        self.fields['fecha_analisis'].widget.attrs.update({
            'placeholder': 'YYYY-MM-DD',
            'class': 'form-control'
        })

    
