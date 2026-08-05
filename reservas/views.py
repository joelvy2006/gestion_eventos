from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets

from .models import Reserva
from .serializers import ReservaSerializer
from .forms import ReservaForm
from espacios.models import Espacio
from organizadores.models import Organizador
from django.utils import timezone


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


@login_required
def lista_reservas(request):
    reservas = Reserva.objects.select_related(
        'espacio', 'organizador'
    ).prefetch_related('pago').all()

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

    return render(request, 'confirmar_reserva.html', {
        'reserva': reserva
    })


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

            # Comprobar solapamiento de fechas con otras reservas (no canceladas)
            inicio = reserva.fecha_inicio
            fin = reserva.fecha_fin
            conflicto = Reserva.objects.filter(
                espacio=espacio
            ).exclude(estado='X').filter(
                fecha_inicio__lt=fin,
                fecha_fin__gt=inicio
            ).exists()

            if conflicto:
                messages.error(request, 'El espacio NO está disponible en las fechas seleccionadas.')
            else:
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


def buscar_espacios(request):
    """Página pública donde el cliente ingresa fechas y obtiene los espacios disponibles."""
    espacios = []
    inicio = None
    fin = None

    if request.method == 'POST':
        inicio_str = request.POST.get('fecha_inicio')
        fin_str = request.POST.get('fecha_fin')
        try:
            inicio = timezone.datetime.fromisoformat(inicio_str)
            fin = timezone.datetime.fromisoformat(fin_str)
        except Exception:
            messages.error(request, 'Formato de fecha inválido.')

        if inicio and fin and fin <= inicio:
            messages.error(request, 'La fecha de fin debe ser posterior a la fecha de inicio.')
        elif inicio and fin:
            # IDs de espacios con conflicto
            conflict_ids = Reserva.objects.filter(
                fecha_inicio__lt=fin,
                fecha_fin__gt=inicio
            ).values_list('espacio_id', flat=True)

            espacios = Espacio.objects.filter(disponible=True).exclude(id__in=conflict_ids)
            if not espacios:
                messages.info(request, 'No hay espacios disponibles en las fechas seleccionadas.')
    return render(request, 'buscar_espacios.html', {
        'espacios': espacios,
        'fecha_inicio': inicio,
        'fecha_fin': fin,
    })