from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['producto', 'calificacion', 'contenido']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'calificacion': forms.Select(choices=[
                ('', _('Selecciona una calificación')),
                (1, '⭐ ' + _('1 estrella')),
                (2, '⭐⭐ ' + _('2 estrellas')),
                (3, '⭐⭐⭐ ' + _('3 estrellas')),
                (4, '⭐⭐⭐⭐ ' + _('4 estrellas')),
                (5, '⭐⭐⭐⭐⭐ ' + _('5 estrellas')),
            ], attrs={
                'class': 'form-select',
                'required': True
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'required': False
            })
        }
        labels = {
            'producto': _('Producto'),
            'calificacion': _('Calificación'),
            'contenido': _('Comentario (Opcional)')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contenido'].widget.attrs['placeholder'] = _('Comentario opcional sobre el producto...')

class BuscarReseñaForm(forms.Form):
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label=_('Buscar')
    )
    
    calificacion = forms.ChoiceField(
        choices=[
            ('', _('Todas las calificaciones')),
            (1, '⭐ ' + _('1 estrella')),
            (2, '⭐⭐ ' + _('2 estrellas')),
            (3, '⭐⭐⭐ ' + _('3 estrellas')),
            (4, '⭐⭐⭐⭐ ' + _('4 estrellas')),
            (5, '⭐⭐⭐⭐⭐ ' + _('5 estrellas')),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label=_('Calificación')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['busqueda'].widget.attrs['placeholder'] = _('Buscar por producto, comentario o cliente...')
