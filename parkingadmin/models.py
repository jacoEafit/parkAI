from django.db import models
from django.contrib.auth.models import User #Importamos modelo Usuario

class Universidad(models.Model):
    unv_id = models.AutoField(primary_key=True)
    unv_nombre = models.CharField(max_length=40)
    unv_direccion = models.CharField(max_length=255)
    unv_telefono = models.CharField(max_length=20)
    unv_correo = models.EmailField()
    unv_logo = models.ImageField(upload_to='logos/')




class Parqueadero(models.Model):
    OPCIONES_ESTADO_PARQUEADERO = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),]
    
    prq_id = models.AutoField(primary_key=True)
    prq_nombre = models.CharField(max_length=40)
    prq_estado = models.CharField(max_length=15, choices=OPCIONES_ESTADO_PARQUEADERO, default='Activo')
    prq_precio_dia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prq_precio_hora = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prq_universidad_id = models.ForeignKey(Universidad, on_delete=models.CASCADE)




class Conjunto_celdas(models.Model):
    cnj_id = models.AutoField(primary_key=True)
    cnj_parqueadero_id = models.ForeignKey(Parqueadero, on_delete=models.CASCADE)




class Celda(models.Model):
    OPCIONES_ESTADO_CELDA = [
        ('Ocupado', 'Ocupado'),
        ('Desocupado', 'Desocupado'),
        ('No disponible','No disponible')]
    
    cld_id = models.AutoField(primary_key=True)
    cld_numero_celda = models.IntegerField() #Numero de celda dentro del parqueadero
    cld_conjunto_celdas_id = models.ForeignKey(Conjunto_celdas, on_delete=models.CASCADE)
    cld_estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO_CELDA, default='Desocupado')
    



class Carnet(models.Model):
    crn_id = models.AutoField(primary_key=True)
    crn_usuario_id = models.ForeignKey(User, on_delete=models.CASCADE) #Usuario al que pertenece carnet
    crn_saldo = models.DecimalField(max_digits=10, decimal_places=2)




class Vehiculo(models.Model):
    vhc_id = models.AutoField(primary_key=True)
    vhc_placa = models.CharField(max_length=15)
    vhc_carnet_id = models.ForeignKey(Carnet, on_delete=models.CASCADE)




class Ingreso(models.Model):
    ing_id = models.AutoField(primary_key=True)
    ing_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    ing_placa_vehiculo = models.CharField(max_length=15)
    ing_fecha_hora = models.DateTimeField()




class Egreso(models.Model):
    egr_id = models.AutoField(primary_key=True)
    egr_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    egr_placa_vehiculo = models.CharField(max_length=15)
    egr_fecha_hora = models.DateTimeField()




class Factura(models.Model):
    fac_id = models.AutoField(primary_key=True)
    fac_vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fac_placa_vehiculo = models.CharField(max_length=15)
    fac_ingreso_id = models.DateTimeField()
    fac_egreso_id = models.DateTimeField()
    fac_precio_neto = models.DecimalField(max_digits=10, decimal_places=2)
