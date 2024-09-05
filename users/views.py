from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  # Autenticar usando username
        if user is not None:
            login(request, user)  # Iniciar sesión
            return redirect('home')  # Redirigir a la página principal o cualquier otra
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')  # Mostrar mensaje de error
    return render(request, 'login.html')  # Renderizar la plantilla de login

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')  # Redirige a la página principal u otra página de tu elección
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def userManagement(request):
    return render(request, 'userManagement.html')
