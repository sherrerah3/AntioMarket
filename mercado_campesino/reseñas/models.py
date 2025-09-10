from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Reseña(models.Model):
    producto = models.ForeignKey("productos.Producto", on_delete=models.CASCADE)
    cliente = models.ForeignKey("cuentas.CuentaCliente", on_delete=models.CASCADE)
    contenido = models.TextField(blank=True, null=True, help_text="Comentario opcional sobre el producto")
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('producto', 'cliente')  # Un cliente solo puede reseñar un producto una vez
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"Reseña de {self.cliente.usuario.username} para {self.producto.nombre} - {self.calificacion}⭐"
