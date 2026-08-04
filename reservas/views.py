from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets

from .models import Reserva
from .serializers import ReservaSerializer
from .forms import ReservaForm
from espacios.models import Espacio
from organizadores.models import Organizador


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


@login_required
def lista_reservas(request):
    reservas = Reserva.objects.select_related(
        'espacio', 'organizador'
    ).all()

    return render(request, 'lista_reservas.html', {
        'reservas': reservas
    })


@login_required
def agregar_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('lista_reservas')
    else:
        form = ReservaForm()

    return render(request, 'agregar_reserva.html', {
        'form': form
    })


@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('lista_reservas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'editar_reserva.html', {
        'form': form,
        'reserva': reserva
    })


@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('lista_reservas')

    return render(request, 'eliminar_reserva.html', {
        'reserva': reserva
    })


@login_required
def confirmar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.estado = 'C'
    reserva.save()

    messages.success(request, 'Reserva confirmada.')

    return redirect('lista_reservas')


@login_required
def cancelar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.estado = 'X'
    reserva.save()

    messages.success(request, 'Reserva cancelada.')

    return redirect('lista_reservas')


# ===========================
# Reserva desde la página pública
# ===========================

def reservar_espacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.espacio = espacio
            reserva.save()

            messages.success(request, 'Reserva realizada correctamente.')
            return redirect('inicio')

    else:
        form = ReservaForm(initial={
            'espacio': espacio
        })

    return render(request, 'reservar_espacio.html', {
        'form': form,
        'espacio': espacio
    })