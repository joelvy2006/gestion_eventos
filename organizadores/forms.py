from django import forms
from django.core.validators import RegexValidator
from .models import Organizador

letters_spaces = RegexValidator(
    regex=r'^[A-Za-zÀ-ÿ\s]+$',
    message='Solo letras y espacios.'
)

letters_numbers_spaces = RegexValidator(
    regex=r'^[A-Za-z0-9À-ÿ\s]*$',
    message='Solo letras, números y espacios.'
)

numbers_only = RegexValidator(
    regex=r'^\d+$',
    message='Solo números.'
)

class OrganizadorForm(forms.ModelForm):
    nombre_completo = forms.CharField(
        label='Nombre completo',
        required=True,
        validators=[letters_spaces],
        error_messages={'required': 'Falta el nombre completo.'},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    institucion = forms.CharField(
        label='Institución',
        required=False,
        validators=[letters_numbers_spaces],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label='Teléfono',
        required=True,
        validators=[numbers_only],
        error_messages={'required': 'Falta el teléfono.'},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo = forms.EmailField(
        label='Correo',
        required=True,
        error_messages={
            'required': 'Falta el correo.',
            'invalid': 'Correo inválido.'
        },
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Organizador
        fields = ['nombre_completo', 'institucion', 'telefono', 'correo']
