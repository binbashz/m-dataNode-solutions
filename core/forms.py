from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
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
    class Meta:
        model = CondicionesCultivo
        fields = ['variedad', 'temperatura', 'humedad', 'tipo_suelo', 'registro_fecha']

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

    