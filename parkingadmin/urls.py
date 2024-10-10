from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home , name="home"), 
    path('sobre_nosotros/', views.sobreNosotros, name="sobre_nosotros"),
    path('lectura_placa_vehiculo/', views.lectura_placa_vehiculo, name="lectura_placa_vehiculo"),
    path('ingreso_vehiculo/', views.ingreso_vehiculo, name="ingreso_vehiculo"),
    path('egreso_vehiculo/', views.egreso_vehiculo, name="egreso_vehiculo"),
    path('parking_management/', views.parking_management, name="parking_management"),
    path('parking_management/<int:parqueadero_id>/', views.informacion_parqueadero, name="informacion_parqueadero"),
    path('parking_management/crear_parqueadero/',views.crear_parqueadero, name="crear_parqueadero"),
]