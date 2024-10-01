from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

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

