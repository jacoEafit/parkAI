from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('addVehicle/', views.addVehicle, name='addVehicle'),
    path('deleteVehicle/', views.deleteVehicle, name='deleteVehicle'),
    path('login/', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.manualLogout, name='logout'),
    path('userManagement/', views.userManagement, name='userManagement'),
    path('organizacionRegister', views.organizacionRegister, name='organizacionRegister'),
    path('no_organizacion', views.no_organizacion, name='no_organizacion'),
]