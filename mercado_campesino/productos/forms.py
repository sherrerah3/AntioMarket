from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .models import Producto

class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    
    CATEGORIAS_CHOICES = [
        ('', _('Selecciona una categoría')),
        ('Alimentos', _('Alimentos')),
        ('Artesanías y Hogar', _('Artesanías y Hogar')),
        ('Moda y Textiles', _('Moda y Textiles')),
        ('Cultivo y Jardín', _('Cultivo y Jardín')),
        ('Bienestar y Cuidado Personal', _('Bienestar y Cuidado Personal')),
    ]
    
    categoria = forms.ChoiceField(
        choices=CATEGORIAS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01'
        })
    )
    
    stock = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0'
        })
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'nombre': _('Nombre del producto'),
            'descripcion': _('Descripción del producto'),
            'precio': _('Precio'),
            'stock': _('Stock'),
            'categoria': _('Categoría'),
            'imagen': _('Imagen')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = _('Nombre del producto')
        self.fields['descripcion'].widget.attrs['placeholder'] = _('Describe tu producto: origen, características, beneficios, etc.')
        self.fields['precio'].widget.attrs['placeholder'] = '0.00'
        self.fields['stock'].widget.attrs['placeholder'] = '0'
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria or categoria == '':
            raise forms.ValidationError(_("Debes seleccionar una categoría."))
        return categoria
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError(_("El nombre debe tener al menos 3 caracteres."))
        return nombre.title()  # Capitaliza la primera letra de cada palabra
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError(_("La descripción debe tener al menos 10 caracteres."))
        return descripcion
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio > 1000000:
            raise forms.ValidationError(_("El precio no puede ser mayor a $1,000,000."))
        return precio
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock > 1000:
            raise forms.ValidationError(_("El stock no puede ser mayor a 1,000 unidades."))
        return stock

class BuscarProductoForm(forms.Form):
    """Formulario para búsqueda de productos"""
    busqueda = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        label=_('Buscar')
    )
    
    categoria = forms.ChoiceField(
        required=False,
        choices=[('', _('Todas las categorías'))] + ProductoForm.CATEGORIAS_CHOICES[1:],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=_('Categoría')
    )
    
    precio_min = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        }),
        label=_('Precio mínimo')
    )
    
    precio_max = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        }),
        label=_('Precio máximo')
    )
    
    ordenar_por = forms.ChoiceField(
        required=False,
        choices=[
            ('', _('Ordenar por...')),
            ('nombre', _('Nombre A-Z')),
            ('-nombre', _('Nombre Z-A')),
            ('precio', _('Precio menor a mayor')),
            ('-precio', _('Precio mayor a menor')),
            ('-id', _('Más recientes')),
            ('id', _('Más antiguos')),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label=_('Ordenar')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['busqueda'].widget.attrs['placeholder'] = _('Buscar productos...')
        self.fields['precio_min'].widget.attrs['placeholder'] = _('Precio mínimo')
        self.fields['precio_max'].widget.attrs['placeholder'] = _('Precio máximo')
    
    def clean(self):
        cleaned_data = super().clean()
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        
        if precio_min and precio_max and precio_min > precio_max:
            raise forms.ValidationError(_("El precio mínimo no puede ser mayor al precio máximo."))
        
        return cleaned_data

class ActualizarStockForm(forms.ModelForm):
    """Formulario simple para actualizar solo el stock"""
    class Meta:
        model = Producto
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            })
        }

class ProductoImagenForm(forms.ModelForm):
    """Formulario para actualizar solo la imagen del producto"""
    class Meta:
        model = Producto
        fields = ['imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
