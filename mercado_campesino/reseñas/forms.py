from django import forms
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
                ('', 'Selecciona una calificación'),
                (1, '⭐ 1 estrella'),
                (2, '⭐⭐ 2 estrellas'),
                (3, '⭐⭐⭐ 3 estrellas'),
                (4, '⭐⭐⭐⭐ 4 estrellas'),
                (5, '⭐⭐⭐⭐⭐ 5 estrellas'),
            ], attrs={
                'class': 'form-select',
                'required': True
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comentario opcional sobre el producto...',
                'required': False
            })
        }
        labels = {
            'producto': 'Producto',
            'calificacion': 'Calificación',
            'contenido': 'Comentario (Opcional)'
        }

class BuscarReseñaForm(forms.Form):
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por producto, comentario o cliente...'
        })
    )
    
    calificacion = forms.ChoiceField(
        choices=[
            ('', 'Todas las calificaciones'),
            (1, '⭐ 1 estrella'),
            (2, '⭐⭐ 2 estrellas'),
            (3, '⭐⭐⭐ 3 estrellas'),
            (4, '⭐⭐⭐⭐ 4 estrellas'),
            (5, '⭐⭐⭐⭐⭐ 5 estrellas'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
