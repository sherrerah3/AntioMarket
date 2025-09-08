from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from productos.models import Producto
from cuentas.models import CuentaCliente
from .models import Carrito, CarritoItem


class CarritoMixin:
    """Mixin para manejar operaciones comunes del carrito"""
    
    def get_cuenta_cliente(self, user):
        """Obtiene la cuenta cliente del usuario"""
        try:
            return CuentaCliente.objects.get(usuario=user)
        except CuentaCliente.DoesNotExist:
            return None
    
    def get_carrito(self, cuenta_cliente):
        """Obtiene o crea el carrito del cliente"""
        carrito, created = Carrito.objects.get_or_create(cliente=cuenta_cliente)
        return carrito


class VerCarritoView(LoginRequiredMixin, CarritoMixin, TemplateView):
    """Vista para mostrar el contenido del carrito del usuario"""
    template_name = 'carrito/ver_carrito.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cuenta_cliente = self.get_cuenta_cliente(self.request.user)
        if not cuenta_cliente:
            messages.error(self.request, 'Necesitas tener una cuenta de cliente para ver el carrito.')
            return context
        
        carrito = self.get_carrito(cuenta_cliente)
        items = CarritoItem.objects.filter(carrito=carrito)
        total = sum(item.subtotal() for item in items)
        
        context.update({
            'carrito': carrito,
            'items': items,
            'total': total,
        })
        return context
    
    def dispatch(self, request, *args, **kwargs):
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            messages.error(request, 'Necesitas tener una cuenta de cliente para ver el carrito.')
            return redirect('productos:home')
        return super().dispatch(request, *args, **kwargs)


class AgregarProductoView(LoginRequiredMixin, CarritoMixin, View):
    """Vista para agregar un producto al carrito"""
    
    def post(self, request, producto_id):
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            messages.error(request, 'Necesitas tener una cuenta de cliente para agregar productos al carrito.')
            return redirect('productos:home')
        
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = self.get_carrito(cuenta_cliente)
        
        # Verificar stock disponible
        if producto.stock <= 0:
            messages.error(request, f'El producto {producto.nombre} está agotado.')
            return redirect('productos:detalle_producto', pk=producto_id)
        
        # Verificar si el producto ya está en el carrito
        item, created = CarritoItem.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': 1}
        )
        
        if not created:
            # Verificar que no exceda el stock disponible
            nueva_cantidad = item.cantidad + 1
            if nueva_cantidad > producto.stock:
                messages.error(request, f'No puedes agregar más unidades. Solo hay {producto.stock} disponibles y ya tienes {item.cantidad} en tu carrito.')
                return redirect('productos:detalle_producto', pk=producto_id)
            
            # Si ya existe, incrementar la cantidad
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, f'Se agregó otra unidad de {producto.nombre} al carrito. Tienes {item.cantidad} unidades.')
        else:
            messages.success(request, f'{producto.nombre} se agregó al carrito.')
        
        return redirect('productos:detalle_producto', pk=producto_id)
    
    def get(self, request, producto_id):
        # Permitir también GET para enlaces directos
        return self.post(request, producto_id)


class ActualizarCantidadView(LoginRequiredMixin, CarritoMixin, View):
    """Vista para actualizar la cantidad de un item en el carrito"""
    
    def post(self, request, item_id):
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            messages.error(request, 'Acceso denegado.')
            return redirect('productos:home')
        
        item = get_object_or_404(CarritoItem, id=item_id, carrito__cliente=cuenta_cliente)
        
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            # Verificar stock disponible
            if cantidad > item.producto.stock:
                messages.error(request, f'No puedes agregar {cantidad} unidades. Solo hay {item.producto.stock} disponibles de {item.producto.nombre}.')
            else:
                item.cantidad = cantidad
                item.save()
                messages.success(request, 'Cantidad actualizada correctamente.')
        else:
            item.delete()
            messages.success(request, 'Producto eliminado del carrito.')
        
        return redirect('carrito:ver_carrito')


class EliminarProductoView(LoginRequiredMixin, CarritoMixin, View):
    """Vista para eliminar un producto del carrito"""
    
    def post(self, request, item_id):
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            messages.error(request, 'Acceso denegado.')
            return redirect('productos:home')
        
        item = get_object_or_404(CarritoItem, id=item_id, carrito__cliente=cuenta_cliente)
        producto_nombre = item.producto.nombre
        item.delete()
        messages.success(request, f'{producto_nombre} se eliminó del carrito.')
        return redirect('carrito:ver_carrito')
    
    def get(self, request, item_id):
        # Permitir también GET para enlaces directos
        return self.post(request, item_id)


class VaciarCarritoView(LoginRequiredMixin, CarritoMixin, View):
    """Vista para vaciar todo el carrito"""
    
    def post(self, request):
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            messages.error(request, 'Acceso denegado.')
            return redirect('productos:home')
        
        carrito = get_object_or_404(Carrito, cliente=cuenta_cliente)
        CarritoItem.objects.filter(carrito=carrito).delete()
        messages.success(request, 'El carrito se vació correctamente.')
        return redirect('carrito:ver_carrito')
    
    def get(self, request):
        # Permitir también GET para enlaces directos
        return self.post(request)


class ContadorCarritoView(LoginRequiredMixin, CarritoMixin, View):
    """Vista AJAX para obtener el contador del carrito"""
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'total_items': 0})
        
        cuenta_cliente = self.get_cuenta_cliente(request.user)
        if not cuenta_cliente:
            return JsonResponse({'total_items': 0})
        
        try:
            carrito = Carrito.objects.get(cliente=cuenta_cliente)
            items = CarritoItem.objects.filter(carrito=carrito)
            total_items = sum(item.cantidad for item in items)
            return JsonResponse({'total_items': total_items})
        except Carrito.DoesNotExist:
            return JsonResponse({'total_items': 0})
