from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from rest_framework import viewsets
from .models import Pago, PagoExtra
from .forms import PagoForm, PagoExtraForm
from .serializers import PagoSerializer
from reservas.models import Reserva


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer


@login_required
def lista_pagos(request):
    pagos = Pago.objects.select_related('reserva').all()
    return render(request, 'lista_pagos.html', {'pagos': pagos})


@login_required
def ver_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    extras_total = pago.extras.aggregate(total=Sum('monto'))['total'] or 0
    valor_reserva = pago.total - extras_total
    return render(request, 'ver_pago.html', {
        'pago': pago,
        'extras_total': extras_total,
        'valor_reserva': valor_reserva,
    })


@login_required
def registrar_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    pago = Pago.objects.filter(reserva=reserva).first()
    if pago is not None and request.method == 'GET':
        return redirect('ver_pago', id=pago.id)

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago_obj = form.save(commit=False)
            pago_obj.reserva = reserva
            pago_obj.save()
            messages.success(request, 'Pago guardado correctamente.')
            return redirect('lista_reservas')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'registrar_pago.html', {
        'reserva': reserva,
        'form': form,
        'editar': bool(pago),
    })


@login_required
def editar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago, disable_total=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm(instance=pago, disable_total=True)
    return render(request, 'registrar_pago.html', {
        'reserva': pago.reserva,
        'form': form,
        'editar': True,
    })


@login_required
def agregar_extra_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    if request.method == 'POST':
        form = PagoExtraForm(request.POST)
        if form.is_valid():
            extra = PagoExtra(
                pago=pago,
                descripcion=form.cleaned_data['descripcion'],
                monto=form.cleaned_data['monto'],
            )
            extra.save()
            pago.total += extra.monto
            pago.save()
            messages.success(request, 'Concepto agregado correctamente al pago.')
            return redirect('ver_pago', id=pago.id)
    else:
        form = PagoExtraForm()
    return render(request, 'agregar_extra_pago.html', {
        'pago': pago,
        'form': form,
    })


@login_required
def eliminar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    if pago.reserva.estado != 'X' and pago.abono < pago.total:
        messages.error(request, 'No se puede eliminar un pago incompleto. Cancela la reserva para eliminarlo.')
        return redirect('lista_pagos')
    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        return redirect('lista_pagos')
    return render(request, 'eliminar_pago.html', {'pago': pago})

# Create your views here.
