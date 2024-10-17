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
    path('parking_management/crear_zona/<int:parqueadero_id>/',views.crear_zona, name="crear_zona"),
    path('parking_management/crear_conjunto_celdas/<int:zona_id>/',views.crear_conjunto_celdas, name="crear_conjunto_celdas"),
    #Eliminar
    path('parking_management/eliminar_parqueadero/<int:parqueadero_id>/',views.eliminar_parqueadero, name="eliminar_parqueadero"),
    path('parking_management/eliminar_zona/<int:zona_id>/',views.eliminar_zona, name="eliminar_zona"),
    path('parking_management/eliminar_conjunto_celdas/<int:conjunto_celdas_id>/',views.eliminar_conjunto_celdas, name="eliminar_conjunto_celdas"),
    #Cálculo espacios vacíos
    #path('parking_management/validar_disponibilidad_celdas/<int:conjunto_id>/',views.validar_disponibilidad_celdas, name="validar_disponibilidad_celdas"),
]
