from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, VehiculoForm, DeleteVehicleForm
from parkingadmin.models import Vehiculo  
from django.shortcuts import get_object_or_404, redirect, render

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
    return render(request, 'login.html')  

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
def manualLogout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('home')  # Redirige a la página principal o a cualquier otra página que desees

@login_required 
def addVehicle(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.vhc_usuario_id = request.user  # Asignar el usuario logueado
            vehiculo.save()
            return redirect('userManagement')
        else:

            for field in form:
                for error in field.errors:
                    messages.error(request, f'Error en {field.label}: {error}')
    
    else:
        form = VehiculoForm()

    return render(request, 'addVehicle.html', {'form': form})

@login_required
def deleteVehicle(request):
    if request.method == 'POST':
        form = DeleteVehicleForm(request.POST)
        if form.is_valid():
            vhc_placa = form.cleaned_data['vhc_placa'].upper() 
            try:
                vehiculo = Vehiculo.objects.get(vhc_placa=vhc_placa, vhc_usuario_id=request.user)
                vehiculo.delete()
                return redirect('userManagement')  
            except Vehiculo.DoesNotExist:
                messages.error(request, 'No se encontró un vehículo con esa placa para el usuario actual.')
    else:
        form = DeleteVehicleForm()
    
    return render(request, 'deleteVehicle.html', {'form': form})

@login_required
def userManagement(request):
    
    # Pedimos el usuario
    user = request.user
    
    # Filtramos los vehiculos del usuario y los pasamos al html
    vehicles = Vehiculo.objects.filter(vhc_usuario_id=user)

    return render(request, 'userManagement.html', {'user': user, 'vehicles': vehicles})

