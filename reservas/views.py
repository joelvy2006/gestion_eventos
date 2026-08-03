from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reserva
from espacios.models import Espacio
from organizadores.models import Organizador


@login_required
def lista_reservas(request):
	reservas = Reserva.objects.select_related('espacio','organizador').all()
	return render(request, 'lista_reservas.html', {'reservas': reservas})


@login_required
def agregar_reserva(request):
	espacios = Espacio.objects.filter(disponible=True)
	organizadores = Organizador.objects.all()
	if request.method == 'POST':
		Reserva.objects.create(
			nombre_evento = request.POST.get('nombre_evento'),
			espacio = Espacio.objects.get(id=request.POST.get('espacio')),
			organizador = Organizador.objects.get(id=request.POST.get('organizador')),
			fecha_inicio = request.POST.get('fecha_inicio'),
			fecha_fin = request.POST.get('fecha_fin'),
			estado = request.POST.get('estado','P')
		)
		return redirect('lista_reservas')
	return render(request, 'agregar_reserva.html', {'espacios':espacios,'organizadores':organizadores})


@login_required
def editar_reserva(request, id):
	r = get_object_or_404(Reserva, id=id)
	espacios = Espacio.objects.filter(disponible=True)
	organizadores = Organizador.objects.all()
	if request.method == 'POST':
		r.nombre_evento = request.POST.get('nombre_evento')
		r.espacio = Espacio.objects.get(id=request.POST.get('espacio'))
		r.organizador = Organizador.objects.get(id=request.POST.get('organizador'))
		r.fecha_inicio = request.POST.get('fecha_inicio')
		r.fecha_fin = request.POST.get('fecha_fin')
		r.estado = request.POST.get('estado', r.estado)
		r.save()
		return redirect('lista_reservas')
	return render(request, 'editar_reserva.html', {'reserva': r, 'espacios':espacios,'organizadores':organizadores})


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
