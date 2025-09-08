from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pedido

class MisPedidosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'pedidos/mis_pedidos.html'
    context_object_name = 'pedidos'
    
    def test_func(self):
        return hasattr(self.request.user, 'cuentacliente')
    
    def get_queryset(self):
        return Pedido.objects.filter(
            cliente=self.request.user.cuentacliente
        ).order_by('-fecha_creacion')