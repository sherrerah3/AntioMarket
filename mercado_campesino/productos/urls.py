from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    # Páginas públicas
    path('', views.HomeView.as_view(), name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('productos/', views.ProductoListView.as_view(), name='lista_productos'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='detalle_producto'),
    
    # Productos por vendedor y categoría
    path('vendedor/<int:vendedor_id>/', views.ProductosPorVendedorView.as_view(), name='productos_por_vendedor'),
    path('categoria/<str:categoria>/', views.ProductosPorCategoriaView.as_view(), name='productos_por_categoria'),
    
    # Panel de vendedor (CRUD productos)
    path('mis-productos/', views.MisProductosView.as_view(), name='mis_productos'),
    path('crear-producto/', views.CrearProductoView.as_view(), name='crear_producto'),
    path('editar-producto/<int:pk>/', views.EditarProductoView.as_view(), name='editar_producto'),
    path('eliminar-producto/<int:pk>/', views.EliminarProductoView.as_view(), name='eliminar_producto'),
]