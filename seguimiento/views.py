from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Pago
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
    if request.method == 'POST':
        total = request.POST.get('total')
        abono = request.POST.get('abono', 0)
        Pago.objects.update_or_create(reserva=reserva, defaults={'total': total, 'abono': abono})
        return redirect('lista_pagos')
    return render(request, 'registrar_pago.html', {'reserva': reserva})
from django.shortcuts import render

# Create your views here.
