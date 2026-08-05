from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    total = forms.DecimalField(
        label='Total',
        required=True,
        max_digits=10,
        decimal_places=2,
        error_messages={'required': 'Falta el total.', 'invalid': 'Total inválido.'},
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    abono = forms.DecimalField(
        label='Abono',
        required=True,
        max_digits=10,
        decimal_places=2,
        error_messages={'required': 'Falta el abono.', 'invalid': 'Abono inválido.'},
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    class Meta:
        model = Pago
        fields = ['total', 'abono']

    def __init__(self, *args, disable_total=False, **kwargs):
        super().__init__(*args, **kwargs)
        if disable_total:
            self.fields['total'].widget.attrs['readonly'] = True
            self.fields['total'].widget.attrs['class'] += ' bg-dark text-white'
            self.fields['total'].widget.attrs['style'] = 'background-color: #000; color: #fff;'

    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total')
        abono = cleaned_data.get('abono')
        if total is not None and abono is not None and abono > total:
            raise forms.ValidationError('El abono no puede ser mayor que el total.')
        return cleaned_data


class PagoExtraForm(forms.Form):
    descripcion = forms.CharField(
        label='Concepto',
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción opcional'})
    )
    monto = forms.DecimalField(
        label='Monto adicional',
        required=True,
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
