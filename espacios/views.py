from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Espacio
from .serializers import EspacioSerializer

class EspacioViewSet(viewsets.ModelViewSet):
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer


def lista_publica(request):
    query = request.GET.get('q', '').strip()
    espacios = Espacio.objects.filter(disponible=True)

    if query:
        espacios = espacios.filter(
            Q(nombre__icontains=query) |
            Q(tipo__icontains=query) |
            Q(ubicacion__icontains=query)
        )

    return render(request, 'lista_publica.html', {
        'espacios': espacios,
        'query': query,
    })


def ver_espacio(request, id):
    espacio = get_object_or_404(Espacio, id=id)
    photos = [
        'img/portfolio/portfolio-1.jpg',
        'img/portfolio/portfolio-2.jpg',
        'img/portfolio/portfolio-3.jpg'
    ]
    return render(request, 'ver_espacio.html', {
        'espacio': espacio,
        'photos': photos
    })

@login_required
def lista_espacios(request):
    espacios = Espacio.objects.all()
    return render(request, 'lista_espacios.html', {'espacios': espacios})

@login_required
def agregar_espacio(request):
    if request.method == 'POST':
        Espacio.objects.create(
            nombre=request.POST['nombre'],
            tipo=request.POST['tipo'],
            capacidad=request.POST['capacidad'],
            costo_hora=request.POST['costo_hora'],
            ubicacion=request.POST['ubicacion'],
            disponible=request.POST.get('disponible') == 'on'
        )
        return redirect('lista_espacios')
    return render(request, 'agregar_espacio.html')

@login_required
def editar_espacio(request, id):
    esp = get_object_or_404(Espacio, id=id)
    if request.method == 'POST':
        esp.nombre = request.POST['nombre']
        esp.tipo = request.POST['tipo']
        esp.capacidad = request.POST['capacidad']
        esp.costo_hora = request.POST['costo_hora']
        esp.ubicacion = request.POST['ubicacion']
        esp.disponible = request.POST.get('disponible') == 'on'
        esp.save()
        return redirect('lista_espacios')
    return render(request, 'editar_espacio.html', {'espacio': esp})

@login_required
def eliminar_espacio(request, id):
    esp = get_object_or_404(Espacio, id=id)
    if request.method == 'POST':
        esp.delete()
        return redirect('lista_espacios')
    return render(request, 'eliminar_espacio.html', {'espacio': esp})

# Create your views here.
