from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home , name="home"), 
    path('sobre_nosotros/', views.sobreNosotros, name="sobre_nosotros"),
    path('lectura_placa_vehiculo/', views.lectura_placa_vehiculo, name="lectura_placa_vehiculo"),
    path('ingreso_vehiculo/', views.ingreso_vehiculo, name="ingreso_vehiculo"),
    path('egreso_vehiculo/', views.egreso_vehiculo, name="egreso_vehiculo"),
]