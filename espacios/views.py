from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Espacio

def lista_publica(request):
    espacios = Espacio.objects.filter(disponible=True)
    return render(request, 'lista_publica.html', {'espacios': espacios})

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
