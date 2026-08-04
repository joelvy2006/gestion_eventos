from rest_framework import serializers
from .models import Pago  # Reemplaza con el nombre exacto de tu modelo si varía

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'