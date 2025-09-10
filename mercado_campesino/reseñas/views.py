from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Reseña
from .forms import ReseñaForm
from productos.models import Producto
from pedidos.models import DetallePedido

class ListaReseñasView(ListView):
    """Vista para listar todas las reseñas"""
    model = Reseña
    template_name = 'reseñas/lista_reseñas.html'
    context_object_name = 'reseñas'
    ordering = ['-fecha']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get('busqueda')
        calificacion = self.request.GET.get('calificacion')
        
        if busqueda:
            queryset = queryset.filter(
                Q(contenido__icontains=busqueda) |
                Q(producto__nombre__icontains=busqueda) |
                Q(cliente__usuario__first_name__icontains=busqueda)
            )
        
        if calificacion:
            queryset = queryset.filter(calificacion=calificacion)
            
        return queryset

class CrearReseñaView(LoginRequiredMixin, CreateView):
    """Vista para crear una nueva reseña"""
    model = Reseña
    form_class = ReseñaForm
    template_name = 'reseñas/crear_reseña.html'
    success_url = reverse_lazy('reseñas:lista_reseñas')
    
    def get_form(self, form_class=None):
        """Filtrar productos solo a los que el usuario ha comprado"""
        form = super().get_form(form_class)
        if hasattr(self.request.user, 'cuentacliente'):
            # Obtener productos que el cliente ha comprado
            productos_comprados = DetallePedido.objects.filter(
                pedido__cliente=self.request.user.cuentacliente,
                pedido__estado='completado'
            ).values_list('producto', flat=True).distinct()
            
            # Excluir productos que ya ha reseñado
            productos_ya_reseñados = Reseña.objects.filter(
                cliente=self.request.user.cuentacliente
            ).values_list('producto', flat=True)
            
            # Filtrar productos disponibles para reseñar
            productos_disponibles = productos_comprados.exclude(
                id__in=productos_ya_reseñados
            )
            
            form.fields['producto'].queryset = Producto.objects.filter(
                id__in=productos_disponibles
            )
            
            if not productos_disponibles.exists():
                form.fields['producto'].queryset = Producto.objects.none()
                
        return form
    
    def form_valid(self, form):
        # Verificar que el usuario haya comprado el producto
        producto = form.cleaned_data['producto']
        cliente = self.request.user.cuentacliente
        
        # Verificar compra previa
        ha_comprado = DetallePedido.objects.filter(
            pedido__cliente=cliente,
            pedido__estado='completado',
            producto=producto
        ).exists()
        
        if not ha_comprado:
            messages.error(self.request, 'Solo puedes reseñar productos que hayas comprado.')
            return self.form_invalid(form)
        
        # Verificar que no haya reseñado ya este producto
        ya_reseñado = Reseña.objects.filter(
            cliente=cliente,
            producto=producto
        ).exists()
        
        if ya_reseñado:
            messages.error(self.request, 'Ya has reseñado este producto.')
            return self.form_invalid(form)
        
        # Asignar el cliente actual
        form.instance.cliente = cliente
        messages.success(self.request, '¡Reseña publicada exitosamente!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si viene desde un producto específico
        producto_id = self.kwargs.get('producto_id')
        if producto_id:
            context['producto'] = get_object_or_404(Producto, id=producto_id)
        
        # Verificar si tiene productos para reseñar
        if hasattr(self.request.user, 'cuentacliente'):
            productos_comprados = DetallePedido.objects.filter(
                pedido__cliente=self.request.user.cuentacliente,
                pedido__estado='completado'
            ).values_list('producto', flat=True).distinct()
            
            productos_ya_reseñados = Reseña.objects.filter(
                cliente=self.request.user.cuentacliente
            ).values_list('producto', flat=True)
            
            productos_disponibles = productos_comprados.exclude(
                id__in=productos_ya_reseñados
            )
            
            context['tiene_productos_para_reseñar'] = productos_disponibles.exists()
        else:
            context['tiene_productos_para_reseñar'] = False
            
        return context

class DetalleReseñaView(DetailView):
    """Vista para ver el detalle de una reseña"""
    model = Reseña
    template_name = 'reseñas/detalle_reseña.html'
    context_object_name = 'reseña'

def crear_reseña_producto(request, producto_id):
    """Vista para crear reseña desde un producto específico"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if not hasattr(request.user, 'cuentacliente'):
        messages.error(request, 'Solo los clientes pueden escribir reseñas.')
        return redirect('productos:detalle_producto', pk=producto.id)
    
    cliente = request.user.cuentacliente
    
    # Verificar que haya comprado el producto
    ha_comprado = DetallePedido.objects.filter(
        pedido__cliente=cliente,
        pedido__estado='completado',
        producto=producto
    ).exists()
    
    if not ha_comprado:
        messages.error(request, 'Solo puedes reseñar productos que hayas comprado.')
        return redirect('productos:detalle_producto', pk=producto.id)
    
    # Verificar que no haya reseñado ya este producto
    ya_reseñado = Reseña.objects.filter(
        cliente=cliente,
        producto=producto
    ).exists()
    
    if ya_reseñado:
        messages.error(request, 'Ya has reseñado este producto.')
        return redirect('productos:detalle_producto', pk=producto.id)
    
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.cliente = cliente
            reseña.producto = producto
            reseña.save()
            messages.success(request, '¡Reseña publicada exitosamente!')
            return redirect('productos:detalle_producto', pk=producto.id)
    else:
        form = ReseñaForm(initial={'producto': producto})
        # Hacer que el campo producto sea readonly
        form.fields['producto'].widget.attrs['disabled'] = True
    
    return render(request, 'reseñas/crear_reseña.html', {
        'form': form,
        'producto': producto
    })
