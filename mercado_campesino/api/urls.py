from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('productos/', views.productos_disponibles, name='productos_disponibles'),
    path('productos-aliados/', views.productos_aliados, name='productos_aliados'),
]