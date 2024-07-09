from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .models import Cultivo
from .models import Variedad, CondicionesCultivo, TratamientoFitofarmaceutico, AnalisisCalidad
from .models import AnalisisCostos
from .models import Muestra, AnalisisProgramado, ResultadoAnalisis, TipoAnalisis
from .models import PlanProduccion, TareaProduccion, ListaMateriales, ItemListaMateriales
from .models import Cliente, Stock,  Venta, Product, GastoOperativo, Pedido
from .models import ListaMateriales, Material, ItemListaMateriales, Miembro, Cuota


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
        
             
class CultivoForm(forms.ModelForm):
    class Meta:
        model = Cultivo
        fields = ['variedad', 'cantidad_plantas', 'area_cultivo', 'luz_intensidad', 'luz_horas', 'temperatura_dia', 'humedad', 'ph']     
    
    
class AnalisisCostosForm(forms.ModelForm):
    class Meta:
        model = AnalisisCostos
        fields = [
            'costo_semilla', 'costo_sustrato', 'costo_energia',
            'costo_agua', 'costo_manobra', 'produccion_gramos', 'presupuesto'
        ]
        widgets = {
            'costo_semilla': forms.NumberInput(attrs={'placeholder': '  Costo de Semilla'}),
            'costo_sustrato': forms.NumberInput(attrs={'placeholder': ' Tierra, Compost, Fibra'}),
            'costo_energia': forms.NumberInput(attrs={'placeholder': ' Costo de Energía'}),
            'costo_agua': forms.NumberInput(attrs={'placeholder': ' Costo de Agua'}),
            'costo_manobra': forms.NumberInput(attrs={'placeholder': ' Costo Mano de Obra'}),
            'produccion_gramos': forms.NumberInput(attrs={'placeholder': ' Gramos Producidos'}),
            'presupuesto': forms.NumberInput(attrs={'placeholder': ' Presupuesto'}),
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

  
# Analisis
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono', 'email']

class MuestraForm(forms.ModelForm):
    tipo = forms.CharField(label='Tipo', required=False)
    fecha_recepcion = forms.DateField(
        label='Fecha de Recepción',
        input_formats=['%d %m %Y'],
        widget=forms.DateInput(attrs={
            'placeholder': 'DD MM AAAA',
            'format': '%d %m %Y',
        }),
    )

    class Meta:
        model = Muestra
        fields = ['codigo', 'cliente', 'tipo', 'fecha_recepcion', 'observaciones']


class AnalisisProgramadoForm(forms.ModelForm):
    tipo_analisis = forms.ModelChoiceField(queryset=TipoAnalisis.objects.all(), label='Tipo de Análisis')
    fecha_programada = forms.DateField(
    input_formats=['%d %m %Y'],  # Formato de entrada DD MM AAAA
    widget=forms.DateInput(attrs={'placeholder': 'DD MM AAAA'}),
    label='Fecha Programada'
    )

    class Meta:
        model = AnalisisProgramado
        fields = ['tipo_analisis', 'fecha_programada', 'prioridad']  
        

class ResultadoAnalisisForm(forms.ModelForm):
    fecha_analisis = forms.DateField(
        input_formats=['%d %m %Y'], 
        widget=forms.DateInput(attrs={'placeholder': 'DD MM AAAA'}),
        label='Fecha de Análisis'
    )
    resultados = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Ingrese los resultados aquí'}),
        label='Resultados'
    )

    class Meta:
        model = ResultadoAnalisis
        fields = ['analisis_programado', 'fecha_analisis', 'resultados', 'observaciones']
        
# Bar code generator an Product registration
class BarcodeForm(forms.Form):
    product_name = forms.CharField(label='Nombre del Producto', max_length=36, help_text='Máximo 36 caracteres')
    product_code = forms.CharField(label='Código del Producto', max_length=15, help_text='Máximo 15 caracteres')
    is_favorite = forms.BooleanField(label='Marcar como favorito', required=False)
    

class GastoOperativoForm(forms.ModelForm):
    class Meta:
        model = GastoOperativo
        fields = ['tipo_gasto', 'descripcion', 'monto', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }       

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'variedad', 'cantidad', 'precio_unitario', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.fields['variedad'].required = False

class PedidoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Product.objects.filter(stock__quantity__gt=0).order_by('name'),
        label="Producto",
        empty_label="Seleccione un producto"
    )
    variedad = forms.ModelChoiceField(
        queryset=Variedad.objects.all(),
        label="Variedad",
        empty_label="Seleccione una variedad",
        required=False 
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Descripción"
    )
    direccion = forms.CharField(
        max_length=200,
        required=False,
        label="Dirección de entrega"
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono de contacto"
    )
    asociar_cliente = forms.BooleanField(
        required=False,
        label="¿Asociar con cliente/miembro registrado?",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all().order_by('nombre'),
        required=False,
        label="Cliente",
        empty_label="Seleccione un cliente"
    )
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.all().order_by('nombre'),
        required=False,
        label="Miembro",
        empty_label="Seleccione un miembro"
    )

    class Meta:
        model = Pedido
        fields = ['producto', 'variedad', 'cantidad', 'fecha_pedido', 'fecha_entrega', 'descripcion', 'direccion', 'telefono', 'asociar_cliente', 'cliente', 'miembro']
        widgets = {
            'fecha_pedido': forms.DateInput(attrs={'type': 'date'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        asociar_cliente = cleaned_data.get('asociar_cliente')
        cliente = cleaned_data.get('cliente')
        miembro = cleaned_data.get('miembro')

        if asociar_cliente:
            if not cliente and not miembro:
                raise forms.ValidationError("Debe seleccionar un cliente o un miembro si desea asociar el pedido.")
            if cliente and miembro:
                raise forms.ValidationError("No puede seleccionar tanto un cliente como un miembro. Elija uno.")
        else:
            # Si no se asocia, limpiamos los campos de cliente y miembro
            cleaned_data['cliente'] = None
            cleaned_data['miembro'] = None

        return cleaned_data


        
class AddToStockForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Producto",
        empty_label="Seleccione un producto"
    )
    quantity = forms.IntegerField(min_value=1, label="Cantidad")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all().order_by('name')
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - {obj.variedad.nombre if obj.variedad else ''} - {obj.code}"
        
class PlanProduccionForm(forms.ModelForm):
    class Meta:
        model = PlanProduccion
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'detalles', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'placeholder': 'AAAA-MM-DD'}),
            'fecha_fin': forms.DateInput(attrs={'placeholder': 'AAAA-MM-DD'}),
        }

class TareaProduccionForm(forms.ModelForm):
    class Meta:
        model = TareaProduccion
        fields = ['nombre', 'descripcion', 'asignado_a', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'placeholder': 'AAAA-MM-DD'}),
            'fecha_fin': forms.DateInput(attrs={'placeholder': 'AAAA-MM-DD'}),
        }

class ListaMaterialesForm(forms.ModelForm):
    materiales = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ListaMateriales
        fields = ['nombre_producto', 'materiales']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['materiales'].initial = self.instance.materiales.all()

    def save(self, commit=True):
        lista_materiales = super().save(commit=False)
        if commit:
            lista_materiales.save()
            self.save_materiales(lista_materiales)
        return lista_materiales

    def save_materiales(self, lista_materiales):
        materiales = self.cleaned_data.get('materiales')
        lista_materiales.materiales.clear()
        for material in materiales:
            ItemListaMateriales.objects.create(
                lista_materiales=lista_materiales,
                material=material,
                cantidad=1  
            )

class ItemListaMaterialesForm(forms.ModelForm):
    class Meta:
        model = ItemListaMateriales
        fields = ['material', 'lista_materiales', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.all()
             

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'apellido', 'email', 'numero_socio', 'fecha_ingreso', 'activo']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }

class CuotaForm(forms.ModelForm):
    PAGADO_CHOICES = [
        (True, 'Pagado'),
        (False, 'Pendiente')
    ]

    pagado = forms.ChoiceField(choices=PAGADO_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Cuota
        fields = ['fecha_pago', 'monto', 'periodo', 'pagado']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }    

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona un producto'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].label = 'Producto'
        self.fields['quantity'].label = 'Cantidad'