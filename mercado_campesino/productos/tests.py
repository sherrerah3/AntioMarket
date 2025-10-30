from django.test import TestCase
from django.urls import reverse
from .models import Producto
from cuentas.models import CuentaVendedor, Usuario

class ProductoTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='vendedor_test',
            password='testpass123',
            email='test@example.com',
            is_vendedor=True
        )
        self.vendedor = CuentaVendedor.objects.create(
            usuario=self.user,
            nombre_tienda='Tienda de Prueba'
        )

    def test_crear_producto(self):
        # Verifica que un producto se creara correctamente
        producto = Producto.objects.create(
            vendedor=self.vendedor,
            nombre='Producto Test',
            descripcion='Descripción de prueba',
            precio=10000,
            stock=5,
            categoria='Alimentos'
        )
        
        self.assertEqual(producto.nombre, 'Producto Test')
        self.assertEqual(producto.stock, 5)
        self.assertEqual(producto.vendedor.nombre_tienda, 'Tienda de Prueba')
        self.assertTrue(producto.precio > 0)

    def test_productos_sin_stock_no_aparecen(self):
        # Verifica que no se muestren los productos sin stock
        producto_con_stock = Producto.objects.create(
            vendedor=self.vendedor,
            nombre='Producto Stock',
            descripcion='Stock > 0',
            precio=15000,
            stock=10,
            categoria='Alimentos'
        )
        
        producto_sin_stock = Producto.objects.create(
            vendedor=self.vendedor,
            nombre='Producto No Stock',
            descripcion='Stock = 0',
            precio=12000,
            stock=0,
            categoria='Alimentos'
        )

        productos_disponibles = Producto.objects.filter(stock__gt=0)
        productos_no_disponibles = Producto.objects.filter(stock=0)
        
        self.assertEqual(productos_disponibles.count(), 1)
        self.assertEqual(productos_no_disponibles.count(), 1)
        self.assertEqual(productos_disponibles.first(), producto_con_stock)
        self.assertEqual(productos_no_disponibles.first(), producto_sin_stock)
        
        self.assertIn(producto_con_stock, productos_disponibles)
        self.assertIn(producto_sin_stock, productos_no_disponibles)

# Ejecutar ambas pruebas:
# python manage.py test productos