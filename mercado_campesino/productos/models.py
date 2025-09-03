from django.db import models
from cuentas.models import CuentaVendedor

# Create your models here.
class Producto(models.Model):
    vendedor = models.ForeignKey(CuentaVendedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.CharField(max_length=50)
    imagen_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre
