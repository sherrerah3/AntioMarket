from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('mis-pedidos/', views.MisPedidosView.as_view(), name='mis_pedidos'),
    path('pedido/<int:pedido_id>/comprobante/<str:tipo>/', 
         views.descargar_comprobante, 
         name='descargar_comprobante'),
]