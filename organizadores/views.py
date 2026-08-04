from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Organizador
from .serializers import OrganizadorSerializer
from .forms import OrganizadorForm

class OrganizadorViewSet(viewsets.ModelViewSet):
    queryset = Organizador.objects.all()
    serializer_class = OrganizadorSerializer


@login_required
def lista_organizadores(request):
    organizadores = Organizador.objects.all()
    return render(request, 'lista_organizadores.html', {'organizadores': organizadores})

@login_required
def agregar_organizador(request):
    if request.method == 'POST':
        form = OrganizadorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organizador creado correctamente.')
            return redirect('lista_organizadores')
    else:
        form = OrganizadorForm()
    return render(request, 'agregar_organizador.html', {'form': form})

@login_required
def editar_organizador(request, id):
    org = get_object_or_404(Organizador, id=id)
    if request.method == 'POST':
        form = OrganizadorForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organizador actualizado correctamente.')
            return redirect('lista_organizadores')
    else:
        form = OrganizadorForm(instance=org)
    return render(request, 'editar_organizador.html', {'form': form, 'organizador': org})

@login_required
def eliminar_organizador(request, id):
    org = get_object_or_404(Organizador, id=id)
    if request.method == 'POST':
        org.delete()
        return redirect('lista_organizadores')
    return render(request, 'eliminar_organizador.html', {'organizador': org})
# Create your views here.
