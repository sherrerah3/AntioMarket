from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Pedido
from .comprobantes import GeneradorChequePDF, GeneradorFacturaPDF

class MisPedidosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'pedidos/mis_pedidos.html'
    context_object_name = 'pedidos'
    
    def test_func(self):
        return hasattr(self.request.user, 'cuentacliente')
    
    def get_queryset(self):
        return Pedido.objects.filter(
            cliente=self.request.user.cuentacliente
        ).order_by('-fecha_creacion')

@login_required
def descargar_comprobante(request, pedido_id, tipo):
    """
    Vista para descargar el comprobante de pago en formato PDF.
    
    Args:
        pedido_id: ID del pedido
        tipo: Tipo de comprobante ('cheque' o 'factura')
    """
    pedido = get_object_or_404(
        Pedido, 
        id=pedido_id, 
        cliente=request.user.cuentacliente
    )
    
    if tipo == 'cheque':
        generador = GeneradorChequePDF()
        filename = f"cheque_pedido_{pedido_id}.pdf"
    else:
        generador = GeneradorFacturaPDF()
        filename = f"factura_pedido_{pedido_id}.pdf"
    
    pdf_bytes = pedido.generar_comprobante(generador)
    
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response