from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Reserva
from .forms import ReservaForm
from espacios.models import Espacio
from organizadores.models import Organizador


@login_required
def lista_reservas(request):
	reservas = Reserva.objects.select_related('espacio','organizador').all()
	return render(request, 'lista_reservas.html', {'reservas': reservas})


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
    return render(request, 'agregar_reserva.html', {'form': form})


@login_required
def editar_reserva(request, id):
    r = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('lista_reservas')
    else:
        form = ReservaForm(instance=r)
    return render(request, 'editar_reserva.html', {'form': form, 'reserva': r})

@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('lista_reservas')
    return render(request, 'eliminar_reserva.html', {'reserva': reserva})

@login_required
def confirmar_reserva(request, id):
    r = get_object_or_404(Reserva, id=id)
    r.estado = 'C'
    r.save()
    return redirect('lista_reservas')


@login_required
def cancelar_reserva(request, id):
	r = get_object_or_404(Reserva, id=id)
	r.estado = 'X'
	r.save()
	return redirect('lista_reservas')



# Create your views here.
