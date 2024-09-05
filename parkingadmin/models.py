from django.db import models
from django.contrib.auth.models import User 

#Extensión de modelo User con rol "Organizacion" con acceso a parkingadmin e información específica
class Organizacion(models.Model):
    org_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #Id será el mismo que usuario asociado
    org_nombre = models.CharField(max_length=40)
    org_direccion = models.CharField(max_length=255)
    org_telefono = models.CharField(max_length=20)
    org_logo = models.ImageField(upload_to='logos/')




class Parqueadero(models.Model):
    OPCIONES_ESTADO_PARQUEADERO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),]
    
    prq_id = models.AutoField(primary_key=True)
    prq_nombre = models.CharField(max_length=40)
    prq_estado = models.CharField(max_length=15, choices=OPCIONES_ESTADO_PARQUEADERO, default='Activo')
    prq_precio_dia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prq_precio_hora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prq_universidad_id = models.ForeignKey(Organizacion, on_delete=models.CASCADE, default=None)




class Zona(models.Model):
    zna_id = models.AutoField(primary_key=True)
    zna_parqueadero_id = models.ForeignKey(Parqueadero, on_delete=models.CASCADE, default=None)




class Conjunto_celdas(models.Model):
    cnj_id = models.AutoField(primary_key=True)
    cnj_parqueadero_id = models.ForeignKey(Zona, on_delete=models.CASCADE,default=None)




class Celda(models.Model):
    OPCIONES_ESTADO_CELDA = [
        ('Ocupado', 'Ocupado'),
        ('Desocupado', 'Desocupado'),
        ('No disponible','No disponible')]
    
    cld_id = models.AutoField(primary_key=True)
    cld_numero_celda = models.IntegerField() #Numero de celda dentro del parqueadero
    cld_conjunto_celdas_id = models.ForeignKey(Conjunto_celdas, on_delete=models.CASCADE,default=None)
    cld_estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO_CELDA, default='Desocupado')




class Vehiculo(models.Model):
    vhc_id = models.AutoField(primary_key=True)
    vhc_placa = models.CharField(max_length=15)
    vhc_usuario_id = models.ForeignKey(User, on_delete=models.CASCADE,default=None)




class Ingreso(models.Model):
    ing_id = models.AutoField(primary_key=True)
    ing_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,default=None)
    ing_placa_vehiculo = models.CharField(max_length=15)
    ing_fecha_hora = models.DateTimeField()




class Egreso(models.Model):
    egr_id = models.AutoField(primary_key=True)
    egr_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,default=None)
    egr_placa_vehiculo = models.CharField(max_length=15)
    egr_fecha_hora = models.DateTimeField()




class Factura(models.Model):
    fac_id = models.AutoField(primary_key=True)
    fac_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fac_placa_vehiculo = models.CharField(max_length=15)
    fac_ingreso_id = models.ForeignKey(Ingreso, on_delete=models.CASCADE, default=None)
    fac_egreso_id = models.ForeignKey(Egreso, on_delete=models.CASCADE,default=None)
    fac_precio_neto = models.DecimalField(max_digits=10, decimal_places=2)
