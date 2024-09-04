from django.urls import path
from . import views

urlpatterns = [
    path('', views.parkingadmin , name="parkingadmin"), 
]

#Vehiculos:
""" path('crear_vehiculo/', views.crear_vehiculo , name="crear_vehiculo"),
    path('eliminar_vehiculo/', views.eliminar_vehiculo , name="eliminar_vehiculo"),
    path('modificar_vehiculo/', views.modificar_vehiculo , name="modificar_vehiculo"),
    #Carnets:
    path('crear_carnet/', views.crear_carnet , name="crear_carnet"),
    path('eliminar_carnet/', views.recargar_carnet , name="recargar_carnet"),
    path('modificar_carnet/', views.modificar_carnet , name="modificar_carnet"),
    path('recargar_carnet/', views.recargar_carnet , name="recargar_carnet"),
    #Parqueaderos:
    
    #Conjunto_celdas:
    
    #Celdas:

    #Ingreso:
    path('registrar_ingreso/', views.registrar_ingreso , name="registrar_ingreso"),

    #Egreso:
    path('registrar_egreso/', views.registrar_egreso , name="registrar_egreso"), 

    #Factura:
    path('generar_factura', views.generar_factura, name="generar_factura"), #Aquí se genera factura y se cobra parqueadero al carnet """