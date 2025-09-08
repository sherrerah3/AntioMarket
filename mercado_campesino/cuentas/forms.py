from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, CuentaCliente, CuentaVendedor, UbicacionVendedor

class RegistroClienteForm(forms.ModelForm):
    """Formulario para registro de clientes"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label="Confirmar Contraseña"
    )
    
    class Meta:
        model = CuentaCliente
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu dirección completa'
            })
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

class RegistroVendedorForm(forms.ModelForm):
    """Formulario para registro de vendedores"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }),
        label="Confirmar Contraseña"
    )
    
    # Campos de ubicación
    departamento = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Antioquia'
        })
    )
    municipio = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Medellín'
        })
    )
    direccion_tienda = forms.CharField(
        max_length=200,
        label="Dirección de la tienda",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dirección donde vendes tus productos'
        })
    )
    descripcion_zona = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describe la zona donde está ubicada tu finca o tienda'
        }),
        label="Descripción de la zona"
    )
    
    class Meta:
        model = CuentaVendedor
        fields = ['nombre_tienda', 'descripcion_tienda']
        widgets = {
            'nombre_tienda': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Finca San José, Verduras del Campo, etc.'
            }),
            'descripcion_tienda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu tienda, productos que vendes, experiencia, etc.'
            })
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

class EditarPerfilClienteForm(forms.ModelForm):
    """Formulario para editar perfil de cliente"""
    class Meta:
        model = CuentaCliente
        fields = ['direccion']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu dirección completa'
            })
        }

class EditarPerfilVendedorForm(forms.ModelForm):
    """Formulario para editar perfil de vendedor"""
    class Meta:
        model = CuentaVendedor
        fields = ['nombre_tienda', 'descripcion_tienda']
        widgets = {
            'nombre_tienda': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Finca San José, Verduras del Campo, etc.'
            }),
            'descripcion_tienda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu tienda, productos que vendes, experiencia, etc.'
            })
        }

class EditarUsuarioForm(forms.ModelForm):
    """Formulario para editar datos básicos del usuario"""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            })
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email ya está registrado por otro usuario.")
        return email

class AgregarUbicacionForm(forms.ModelForm):
    """Formulario para agregar nuevas ubicaciones a vendedores"""
    class Meta:
        model = UbicacionVendedor
        fields = ['departamento', 'municipio', 'direccion', 'descripcion_zona']
        widgets = {
            'departamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Antioquia'
            }),
            'municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Medellín'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección específica'
            }),
            'descripcion_zona': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe la zona de esta ubicación'
            })
        }
