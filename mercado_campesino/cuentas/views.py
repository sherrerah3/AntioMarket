from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Usuario, CuentaCliente, CuentaVendedor, UbicacionVendedor
from productos.models import Producto
from .forms import (
    RegistroClienteForm, 
    RegistroVendedorForm,
    EditarPerfilClienteForm,
    EditarPerfilVendedorForm,
    EditarUsuarioForm,
    AgregarUbicacionForm
)

# Create your views here.

class AgregarUbicacionView(LoginRequiredMixin, CreateView):
    model = UbicacionVendedor
    form_class = AgregarUbicacionForm
    template_name = 'cuentas/agregar_ubicacion.html'
    success_url = reverse_lazy('cuentas:perfil_vendedor')

    def form_valid(self, form):
        try:
            ubicacion = form.save(commit=False)
            ubicacion.vendedor = self.request.user.cuentavendedor
            ubicacion.departamento = 'Antioquia'
            ubicacion.save()
            messages.success(self.request, 'Nueva ubicación agregada exitosamente.')
            return super().form_valid(form)
        except Exception as e:
            print(f"Error al guardar ubicación: {str(e)}")  # Para debugging
            messages.error(self.request, 'Error al guardar la ubicación.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar Nueva Ubicación'
        return context

class ListaVendedoresView(ListView):
    model = CuentaVendedor
    template_name = 'cuentas/lista_vendedores.html'
    context_object_name = 'vendedores'
    
class DetalleVendedorView(DetailView):
    model = CuentaVendedor
    template_name = 'cuentas/detalle_vendedor.html'
    context_object_name = 'vendedor'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.filter(vendedor=self.object)
        return context

# Views de autenticación
class CustomLoginView(LoginView):
    template_name = 'cuentas/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('productos:home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('productos:home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return super().dispatch(request, *args, **kwargs)

# Views de registro
class RegistroClienteView(CreateView):
    form_class = RegistroClienteForm
    template_name = 'cuentas/registro_cliente.html'
    success_url = reverse_lazy('cuentas:login')
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Crear usuario
                usuario = Usuario.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    is_cliente=True
                )
                
                # Crear cuenta cliente
                cuenta_cliente = form.save(commit=False)
                cuenta_cliente.usuario = usuario
                cuenta_cliente.save()
                
                messages.success(self.request, 'Cliente registrado exitosamente. Ahora puedes iniciar sesión.')
                return redirect(self.success_url)
                
        except Exception as e:
            messages.error(self.request, f'Error al registrar cliente: {str(e)}')
            return self.form_invalid(form)

class RegistroVendedorView(CreateView):
    form_class = RegistroVendedorForm
    template_name = 'cuentas/registro_vendedor.html'
    success_url = reverse_lazy('cuentas:login')
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Crear usuario
                usuario = Usuario.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    is_vendedor=True
                )
                
                # Crear cuenta vendedor
                cuenta_vendedor = form.save(commit=False)
                cuenta_vendedor.usuario = usuario
                cuenta_vendedor.save()
                
                # Crear ubicación del vendedor
                UbicacionVendedor.objects.create(
                    vendedor=cuenta_vendedor,
                    departamento=form.cleaned_data['departamento'],
                    municipio=form.cleaned_data['municipio'],
                    direccion=form.cleaned_data['direccion_tienda'],
                    descripcion_zona=form.cleaned_data['descripcion_zona']
                )
                
                messages.success(self.request, 'Vendedor registrado exitosamente. Ahora puedes iniciar sesión.')
                return redirect(self.success_url)
                
        except Exception as e:
            messages.error(self.request, f'Error al registrar vendedor: {str(e)}')
            return self.form_invalid(form)

# Views de perfil
class PerfilClienteView(LoginRequiredMixin, DetailView):
    model = CuentaCliente
    template_name = 'cuentas/perfil_cliente.html'
    context_object_name = 'cuenta'
    
    def get_object(self):
        return self.request.user.cuentacliente

class PerfilVendedorView(LoginRequiredMixin, DetailView):
    model = CuentaVendedor
    template_name = 'cuentas/perfil_vendedor.html'
    context_object_name = 'cuenta'
    
    def get_object(self):
        return self.request.user.cuentavendedor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ubicaciones'] = self.object.ubicacionvendedor_set.all()
        context['productos'] = self.object.producto_set.all()
        return context

# View general de perfil que redirecciona según el tipo de usuario
class PerfilView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'cuentas/perfil.html'
    
    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_cliente:
            return redirect('cuentas:perfil_cliente')
        elif user.is_vendedor:
            return redirect('cuentas:perfil_vendedor')
        else:
            messages.error(request, 'Tu cuenta no tiene un tipo definido.')
            return redirect('productos:home')

# Views de edición de perfil
class EditarPerfilClienteView(LoginRequiredMixin, UpdateView):
    model = CuentaCliente
    form_class = EditarPerfilClienteForm
    template_name = 'cuentas/editar_perfil_cliente.html'
    success_url = reverse_lazy('cuentas:perfil_cliente')
    
    def get_object(self):
        return self.request.user.cuentacliente
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tipo_usuario': 'cliente',
            'descripcion_header': 'Actualiza tu información personal',
            'icono_seccion': 'fas fa-user',
            'titulo_seccion': 'Información Personal',
            'url_cancelar': reverse_lazy('cuentas:perfil_cliente')
        })
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

class EditarPerfilVendedorView(LoginRequiredMixin, UpdateView):
    model = CuentaVendedor
    form_class = EditarPerfilVendedorForm
    template_name = 'cuentas/editar_perfil_vendedor.html'
    success_url = reverse_lazy('cuentas:perfil_vendedor')
    
    def get_object(self):
        return self.request.user.cuentavendedor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tipo_usuario': 'vendedor',
            'descripcion_header': 'Actualiza la información de tu tienda',
            'icono_seccion': 'fas fa-store',
            'titulo_seccion': 'Información de la Tienda',
            'url_cancelar': reverse_lazy('cuentas:perfil_vendedor')
        })
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)
