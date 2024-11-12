from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, VehiculoForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)  
        if user is not None:
            login(request, user)  
            return redirect('home')  
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')  
    return render(request, 'login.html')  #

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Registro no exitoso, por favor vuelve a intentarlo.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def userManagement(request):
    return render(request, 'userManagement.html')

@login_required
def vehicleManagement(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.vhc_usuario_id = request.user  # Asignar el usuario logueado
            vehiculo.save()
            messages.success(request, 'Vehículo agregado con éxito.')  # Mensaje de éxito
        else:
            # Si el formulario no es válido, puedes agregar mensajes de error
            for field in form:
                for error in field.errors:
                    messages.error(request, f'Error en {field.label}: {error}')
    
    else:
        form = VehiculoForm()

    return render(request, 'vehicleManagement.html', {'form': form})

