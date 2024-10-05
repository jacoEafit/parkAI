from django.contrib import admin
from .models import Vehiculo

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('vhc_id', 'vhc_placa', 'vhc_usuario_id')  # Los campos que quieres mostrar en el admin
