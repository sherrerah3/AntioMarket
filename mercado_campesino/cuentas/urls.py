from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Registro
    path('registro/cliente/', views.RegistroClienteView.as_view(), name='registro_cliente'),
    path('registro/vendedor/', views.RegistroVendedorView.as_view(), name='registro_vendedor'),
    
    # Perfiles
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/cliente/', views.PerfilClienteView.as_view(), name='perfil_cliente'),
    path('perfil/vendedor/', views.PerfilVendedorView.as_view(), name='perfil_vendedor'),
    
    # Edición de perfiles
    path('perfil/cliente/editar/', views.EditarPerfilClienteView.as_view(), name='editar_perfil_cliente'),
    path('perfil/vendedor/editar/', views.EditarPerfilVendedorView.as_view(), name='editar_perfil_vendedor'),
]