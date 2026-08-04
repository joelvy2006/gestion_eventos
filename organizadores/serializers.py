from rest_framework import serializers
from .models import Organizador  # Reemplaza con el nombre exacto de tu modelo si varía

class OrganizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizador
        fields = '__all__'