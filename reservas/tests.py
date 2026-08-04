from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from espacios.models import Espacio
from organizadores.models import Organizador
from reservas.forms import ReservaForm
from reservas.models import Reserva


class ReservaFormTests(TestCase):
    def setUp(self):
        self.espacio = Espacio.objects.create(
            nombre='Salón Principal',
            tipo='salon',
            capacidad=50,
            costo_hora=120.00,
            ubicacion='Piso 1',
            disponible=True,
        )
        self.organizador = Organizador.objects.create(
            nombre_completo='Carlos Pérez',
            institucion='Empresa Demo',
            telefono='987654321',
            correo='carlos@example.com',
        )

    def test_overlapping_reservation_for_same_space_is_rejected(self):
        inicio = timezone.now() + timedelta(days=1, hours=10)
        fin = inicio + timedelta(hours=2)

        Reserva.objects.create(
            nombre_evento='Evento existente',
            espacio=self.espacio,
            organizador=self.organizador,
            fecha_inicio=inicio,
            fecha_fin=fin,
            estado='P',
        )

        form_data = {
            'nombre_evento': 'Evento nuevo',
            'espacio': self.espacio.id,
            'organizador': self.organizador.id,
            'fecha_inicio': (inicio + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'fecha_fin': (fin + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'estado': 'P',
        }

        form = ReservaForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('No se puede reservar', str(form.non_field_errors()))
