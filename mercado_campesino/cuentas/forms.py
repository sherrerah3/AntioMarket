from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Usuario, CuentaCliente, CuentaVendedor, UbicacionVendedor
from .antioquia_data import MUNICIPIOS_ANTIOQUIA

class RegistroClienteForm(forms.ModelForm):
    """Formulario para registro de clientes"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label=_('Nombre de usuario')
    )
    first_name = forms.CharField(
        max_length=30,
        label=_("Nombre"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label=_("Apellido"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        label=_('Correo electrónico')
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        label=_("Contraseña")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        label=_("Confirmar Contraseña")
    )
    
    class Meta:
        model = CuentaCliente
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'direccion': _('Dirección')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Nombre de usuario')
        self.fields['first_name'].widget.attrs['placeholder'] = _('Tu nombre')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Tu apellido')
        self.fields['email'].widget.attrs['placeholder'] = _('tu@email.com')
        self.fields['password1'].widget.attrs['placeholder'] = _('Contraseña')
        self.fields['password2'].widget.attrs['placeholder'] = _('Confirmar contraseña')
        self.fields['direccion'].widget.attrs['placeholder'] = _('Tu dirección completa')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Este nombre de usuario ya está en uso."))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este email ya está registrado."))
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Las contraseñas no coinciden"))
        return password2

class RegistroVendedorForm(forms.ModelForm):
    """Formulario para registro de vendedores"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        label=_('Nombre de usuario')
    )
    first_name = forms.CharField(
        max_length=30,
        label=_("Nombre"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label=_("Apellido"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        label=_('Correo electrónico')
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        label=_("Contraseña")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        label=_("Confirmar Contraseña")
    )
    
    # Campos de ubicación
    departamento = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': True,
            'value': 'Antioquia'
        }),
        label=_('Departamento')
    )
    municipio = forms.ChoiceField(
        choices=[('', _('Seleccione un municipio'))] + MUNICIPIOS_ANTIOQUIA,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_municipio'
        }),
        label=_('Municipio')
    )
    direccion_tienda = forms.CharField(
        max_length=200,
        label=_("Dirección de la tienda"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    descripcion_zona = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
        }),
        label=_("Descripción de la zona")
    )
    
    class Meta:
        model = CuentaVendedor
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2', 'departamento', 'municipio',
            'nombre_tienda', 'descripcion_tienda', 'direccion_tienda'
        ]
        widgets = {
            'nombre_tienda': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion_tienda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            }),
            'direccion_tienda': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'nombre_tienda': _('Nombre de la tienda'),
            'descripcion_tienda': _('Descripción de la tienda'),
            'direccion_tienda': _('Dirección de la tienda')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('Nombre de usuario')
        self.fields['first_name'].widget.attrs['placeholder'] = _('Tu nombre')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Tu apellido')
        self.fields['email'].widget.attrs['placeholder'] = _('tu@email.com')
        self.fields['password1'].widget.attrs['placeholder'] = _('Contraseña')
        self.fields['password2'].widget.attrs['placeholder'] = _('Confirmar contraseña')
        self.fields['direccion_tienda'].widget.attrs['placeholder'] = _('Dirección donde vendes tus productos')
        self.fields['descripcion_zona'].widget.attrs['placeholder'] = _('Describe la zona donde está ubicada tu finca o tienda')
        self.fields['nombre_tienda'].widget.attrs['placeholder'] = _('Ej: Finca San José, Verduras del Campo, etc.')
        self.fields['descripcion_tienda'].widget.attrs['placeholder'] = _('Describe tu tienda, productos que vendes, experiencia, etc.')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Este nombre de usuario ya está en uso."))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este email ya está registrado."))
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Las contraseñas no coinciden"))
        return password2

class EditarPerfilClienteForm(forms.ModelForm):
    """Formulario para editar perfil de cliente"""
    class Meta:
        model = CuentaCliente
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'direccion': _('Dirección')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs['placeholder'] = _('Tu dirección completa')

class EditarPerfilVendedorForm(forms.ModelForm):
    """Formulario para editar perfil de vendedor"""
    class Meta:
        model = CuentaVendedor
        fields = ['nombre_tienda', 'descripcion_tienda']
        widgets = {
            'nombre_tienda': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion_tienda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
            })
        }
        labels = {
            'nombre_tienda': _('Nombre de la tienda'),
            'descripcion_tienda': _('Descripción de la tienda')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_tienda'].widget.attrs['placeholder'] = _('Ej: Finca San José, Verduras del Campo, etc.')
        self.fields['descripcion_tienda'].widget.attrs['placeholder'] = _('Describe tu tienda, productos que vendes, experiencia, etc.')

class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar datos básicos del usuario"""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'first_name': _('Nombre'),
            'last_name': _('Apellido'),
            'email': _('Correo electrónico')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = _('Tu nombre')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Tu apellido')
        self.fields['email'].widget.attrs['placeholder'] = _('tu@email.com')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(_("Este email ya está registrado por otro usuario."))
        return email

class AgregarUbicacionForm(forms.ModelForm):
    municipio = forms.ChoiceField(
        choices=[
            ('', _('Seleccione un municipio')),
            ('Medellín', 'Medellín'),
            ('Bello', 'Bello'),
            ('Envigado', 'Envigado'),
            ('Itagüí', 'Itagüí'),
            ('Sabaneta', 'Sabaneta'),
            ('La Estrella', 'La Estrella'),
            ('Caldas', 'Caldas'),
            ('Copacabana', 'Copacabana'),
            ('Girardota', 'Girardota'),
            ('Barbosa', 'Barbosa'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Municipio')
    )

    class Meta:
        model = UbicacionVendedor
        fields = ['municipio', 'direccion', 'descripcion_zona']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'descripcion_zona': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            })
        }
        labels = {
            'direccion': _('Dirección'),
            'descripcion_zona': _('Descripción de la zona')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs['placeholder'] = _('Ingresa la dirección específica')
        self.fields['descripcion_zona'].widget.attrs['placeholder'] = _('Describe la zona (referencias, puntos cercanos, etc.)')
