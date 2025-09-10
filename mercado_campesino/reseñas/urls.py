from django.urls import path
from . import views

app_name = 'reseñas'

urlpatterns = [
    path('', views.ListaReseñasView.as_view(), name='lista_reseñas'),
    path('crear/', views.CrearReseñaView.as_view(), name='crear_reseña'),
    path('crear/producto/<int:producto_id>/', views.crear_reseña_producto, name='crear_reseña_producto'),
    path('<int:pk>/', views.DetalleReseñaView.as_view(), name='detalle_reseña'),
]