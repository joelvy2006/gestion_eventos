from django import forms
from .models import Reserva
from espacios.models import Espacio
from organizadores.models import Organizador

class ReservaForm(forms.ModelForm):
    nombre_evento = forms.CharField(
        label='Nombre del evento',
        required=True,
        error_messages={'required': 'Falta el nombre del evento.'},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    espacio = forms.ModelChoiceField(
        label='Espacio',
        queryset=Espacio.objects.none(),
        required=True,
        error_messages={'required': 'Selecciona un espacio.'},
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    organizador = forms.ModelChoiceField(
        label='Organizador',
        queryset=Organizador.objects.all(),
        required=True,
        error_messages={'required': 'Selecciona un organizador.'},
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_inicio = forms.DateTimeField(
        label='Fecha de inicio',
        required=True,
        error_messages={'required': 'Falta la fecha de inicio.', 'invalid': 'Formato de fecha inválido.'},
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    fecha_fin = forms.DateTimeField(
        label='Fecha de fin',
        required=True,
        error_messages={'required': 'Falta la fecha de fin.', 'invalid': 'Formato de fecha inválido.'},
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    estado = forms.ChoiceField(
        label='Estado',
        choices=Reserva.ESTADOS,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Reserva
        fields = ['nombre_evento', 'espacio', 'organizador', 'fecha_inicio', 'fecha_fin', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['espacio'].queryset = Espacio.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        if inicio and fin and fin <= inicio:
            raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        return cleaned_data
