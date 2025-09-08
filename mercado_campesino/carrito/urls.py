from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.VerCarritoView.as_view(), name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.AgregarProductoView.as_view(), name='agregar_producto'),
    path('actualizar/<int:item_id>/', views.ActualizarCantidadView.as_view(), name='actualizar_cantidad'),
    path('eliminar/<int:item_id>/', views.EliminarProductoView.as_view(), name='eliminar_producto'),
    path('vaciar/', views.VaciarCarritoView.as_view(), name='vaciar_carrito'),
    path('contador/', views.ContadorCarritoView.as_view(), name='contador_carrito'),
]