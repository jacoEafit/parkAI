from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
