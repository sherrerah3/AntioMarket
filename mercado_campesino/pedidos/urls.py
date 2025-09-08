from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('mis-pedidos/', views.MisPedidosView.as_view(), name='mis_pedidos'),
]