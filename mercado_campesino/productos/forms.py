from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Producto

class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    
    CATEGORIAS_CHOICES = [
        ('', 'Selecciona una categoría'),
        ('Alimentos', 'Alimentos'),
        ('Artesanías y Hogar', 'Artesanías y Hogar'),
        ('Moda y Textiles', 'Moda y Textiles'),
        ('Cultivo y Jardín', 'Cultivo y Jardín'),
        ('Bienestar y Cuidado Personal', 'Bienestar y Cuidado Personal'),
    ]
    
    categoria = forms.ChoiceField(
        choices=CATEGORIAS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'data-placeholder': 'Selecciona una categoría'
        })
    )
    
    precio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0.01'
        })
    )
    
    stock = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
            'min': '0'
        })
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu producto: origen, características, beneficios, etc.'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria or categoria == '':
            raise forms.ValidationError("Debes seleccionar una categoría.")
        return categoria
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre.title()  # Capitaliza la primera letra de cada palabra
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion
    
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio > 1000000:
            raise forms.ValidationError("El precio no puede ser mayor a $1,000,000.")
        return precio
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock > 1000:
            raise forms.ValidationError("El stock no puede ser mayor a 1,000 unidades.")
        return stock

class BuscarProductoForm(forms.Form):
    """Formulario para búsqueda de productos"""
    busqueda = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...',
            'autocomplete': 'off'
        })
    )
    
    categoria = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas las categorías')] + ProductoForm.CATEGORIAS_CHOICES[1:],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    precio_min = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo',
            'step': '0.01',
            'min': '0'
        })
    )
    
    precio_max = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo',
            'step': '0.01',
            'min': '0'
        })
    )
    
    ordenar_por = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Ordenar por...'),
            ('nombre', 'Nombre A-Z'),
            ('-nombre', 'Nombre Z-A'),
            ('precio', 'Precio menor a mayor'),
            ('-precio', 'Precio mayor a menor'),
            ('-id', 'Más recientes'),
            ('id', 'Más antiguos'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        
        if precio_min and precio_max and precio_min > precio_max:
            raise forms.ValidationError("El precio mínimo no puede ser mayor al precio máximo.")
        
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
