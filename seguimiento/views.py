from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from .forms import PagoForm
from reservas.models import Reserva


@login_required
def lista_pagos(request):
    pagos = Pago.objects.select_related('reserva').all()
    return render(request, 'lista_pagos.html', {'pagos': pagos})


@login_required
def ver_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    return render(request, 'ver_pago.html', {'pago': pago})


@login_required
def registrar_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    pago = Pago.objects.filter(reserva=reserva).first()
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago_obj = form.save(commit=False)
            pago_obj.reserva = reserva
            pago_obj.save()
            messages.success(request, 'Pago guardado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'registrar_pago.html', {'reserva': reserva, 'form': form})

# Create your views here.
