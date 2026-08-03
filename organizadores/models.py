from django.db import models
class Organizador(models.Model):
    nombre_completo = models.CharField(max_length=200)
    institucion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    def __str__(self): return self.nombre_completo
# Create your models here.
