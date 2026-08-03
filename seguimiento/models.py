from django.db import models
from reservas.models import Reserva
class Pago(models.Model):
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    abono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    def save(self, *args, **kwargs):
        self.saldo = self.total - self.abono
        super().save(*args,**kwargs)
    def __str__(self): return f"Pago: {self.reserva.nombre_evento}"

# Create your models here.
