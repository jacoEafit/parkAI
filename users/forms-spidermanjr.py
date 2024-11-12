from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from parkingadmin.models import Vehiculo  # Importa el modelo Vehiculo
import re  # Importa el módulo re para expresiones regulares
from parkingadmin.models import Organizacion

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma tu contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):  
        username = self.cleaned_data['username']
        if not username.isalnum():
            raise ValidationError("El nombre de usuario solo puede contener letras y números.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_password2(self):  
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['vhc_placa']  # Solo incluimos el campo vhc_placa en el formulario

    def clean_vhc_placa(self):
        vhc_placa = self.cleaned_data.get('vhc_placa')
        
        # Validar que el campo no esté vacío
        if not vhc_placa:
            raise forms.ValidationError("El campo 'Placa' no puede estar vacío.")
        
        # Convertir a minúsculas
        vhc_placa = vhc_placa.upper()
        
        # Validar que no contenga espacios y solo letras y números
        if not re.match(r'^[A-Z0-9]+$', vhc_placa):  # Cambiar a mayúsculas en la expresión regular
            raise forms.ValidationError("La placa solo puede contener letras y números, sin espacios.")
        
        
        return vhc_placa

class DeleteVehicleForm(forms.Form):
    vhc_placa = forms.CharField(
        label='Placa del vehículo',
        max_length=10,  # Ajusta según el formato de la placa
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese la placa del vehículo',
            'pattern': '[A-Z0-9-]+',  # Modifica según tus necesidades
        })
    )