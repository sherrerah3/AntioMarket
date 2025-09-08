from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    is_cliente = models.BooleanField(default=False)
    is_vendedor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class CuentaCliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Cliente: {self.usuario.username}"

class CuentaVendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre_tienda = models.CharField(max_length=150, default='Mi Tienda')
    descripcion_tienda = models.TextField()
    
    def __str__(self):
        return f"Vendedor: {self.nombre_tienda} ({self.usuario.username})"

class UbicacionVendedor(models.Model):
    vendedor = models.ForeignKey(CuentaVendedor, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    descripcion_zona = models.TextField()
    
    def __str__(self):
        return f"{self.departamento} - {self.municipio}"