from django.db import models
class Espacio(models.Model):
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    costo_hora = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)
    def __str__(self): return self.nombre

# Create your models here.
