from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Organizador

@login_required
def lista_organizadores(request):
    organizadores = Organizador.objects.all()
    return render(request, 'lista_organizadores.html', {'organizadores': organizadores})

@login_required
def agregar_organizador(request):
    if request.method == 'POST':
        Organizador.objects.create(
            nombre_completo = request.POST['nombre_completo'],
            institucion = request.POST['institucion'],
            telefono = request.POST['telefono'],
            correo = request.POST['correo']
        )
        return redirect('lista_organizadores')
    return render(request, 'agregar_organizador.html')

@login_required
def editar_organizador(request, id):
    org = get_object_or_404(Organizador, id=id)
    if request.method == 'POST':
        org.nombre_completo = request.POST['nombre_completo']
        org.institucion = request.POST['institucion']
        org.telefono = request.POST['telefono']
        org.correo = request.POST['correo']
        org.save()
        return redirect('lista_organizadores')
    return render(request, 'editar_organizador.html', {'organizador': org})

@login_required
def eliminar_organizador(request, id):
    org = get_object_or_404(Organizador, id=id)
    if request.method == 'POST':
        org.delete()
        return redirect('lista_organizadores')
    return render(request, 'eliminar_organizador.html', {'organizador': org})
# Create your views here.
