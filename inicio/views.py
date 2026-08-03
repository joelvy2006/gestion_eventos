from django.shortcuts import render
from espacios.models import Espacio
def inicio(request):
    espacios = Espacio.objects.filter(disponible=True)
    return render(request, 'inicio.html', {'espacios': espacios})

# Create your views here.
