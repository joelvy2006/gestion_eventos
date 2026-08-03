from django.shortcuts import render
from espacios.models import Espacio
def inicio(request):
    espacios = Espacio.objects.filter(disponible=True)
    return render(request, 'inicio.html', {'espacios': espacios})

def servicios(request):
    return render(request, 'servicios.html')

def equipo(request):
    return render(request, 'equipo.html')

def testimonios(request):
    return render(request, 'testimonios.html')

def faq(request):
    return render(request, 'faq.html')

def contacto(request):
    return render(request, 'contacto.html')

# Create your views here.
