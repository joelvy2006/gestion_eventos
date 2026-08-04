from rest_framework import serializers
from .models import Reserva  # Reemplaza con el nombre exacto de tu modelo si varía

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'