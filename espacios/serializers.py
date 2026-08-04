from rest_framework import serializers
from .models import Espacio  # Reemplaza con el nombre exacto de tu modelo si varía

class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = '__all__'