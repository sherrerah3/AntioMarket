from django.db import models

# Create your models here.
class Reseña(models.Model):
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE)
    cliente = models.ForeignKey("cuentas.CuentaCliente", on_delete=models.CASCADE)
    contenido = models.TextField()
    calificacion = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.cliente.usuario.username} para {self.producto.nombre}"
