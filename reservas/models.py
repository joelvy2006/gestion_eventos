from django.db import models
from espacios.models import Espacio
from organizadores.models import Organizador
class Reserva(models.Model):
    ESTADOS = [('P','Pendiente'),('C','Confirmada'),('X','Cancelada')]
    nombre_evento = models.CharField(max_length=250)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    def __str__(self): return self.nombre_evento

# Create your models here.
