from django.db import models

class Vehiculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)


class Celda(models.Model):
    numero = models.CharField(max_length=10, unique=True)
    disponible = models.BooleanField(default=True)
    








