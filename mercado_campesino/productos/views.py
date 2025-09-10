from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Producto
from .forms import ProductoForm, BuscarProductoForm, ActualizarStockForm, ProductoImagenForm
from cuentas.models import CuentaVendedor

# Create your views here.

class HomeView(ListView):
    model = Producto
    template_name = 'productos/home.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        form = BuscarProductoForm(self.request.GET)
        
        # Obtener filtros de categoría y búsqueda
        categoria = self.request.GET.get('categoria')
        busqueda = self.request.GET.get('buscar')
        
        # Aplicar filtro por categoría
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        # Aplicar filtro de búsqueda
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(descripcion__icontains=busqueda)
            )
        
        # Aplicar otros filtros del form si existen
        if form.is_valid():
            if form.cleaned_data.get('precio_min'):
                queryset = queryset.filter(precio__gte=form.cleaned_data['precio_min'])
            if form.cleaned_data.get('precio_max'):
                queryset = queryset.filter(precio__lte=form.cleaned_data['precio_max'])
            
        return queryset.order_by('-id')  # Ordenar por más recientes primero
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar categorías únicas al contexto
        context['categorias'] = Producto.objects.values_list('categoria', flat=True).distinct()
        # Agregar el formulario de búsqueda
        context['form'] = BuscarProductoForm(self.request.GET)
        return context

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle_producto.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Productos relacionados del mismo vendedor
        context['productos_relacionados'] = Producto.objects.filter(
            vendedor=self.object.vendedor,
            stock__gt=0
        ).exclude(id=self.object.id)[:4]
        
        # Verificar si el usuario tiene este producto en su carrito
        if self.request.user.is_authenticated and hasattr(self.request.user, 'cuentacliente'):
            from carrito.models import Carrito, CarritoItem
            try:
                carrito = Carrito.objects.get(cliente=self.request.user.cuentacliente)
                carrito_item = CarritoItem.objects.filter(carrito=carrito, producto=self.object).first()
                if carrito_item:
                    context['cantidad_en_carrito'] = carrito_item.cantidad
                    context['stock_disponible'] = self.object.stock - carrito_item.cantidad
                else:
                    context['cantidad_en_carrito'] = 0
                    context['stock_disponible'] = self.object.stock
            except Carrito.DoesNotExist:
                context['cantidad_en_carrito'] = 0
                context['stock_disponible'] = self.object.stock
        else:
            context['cantidad_en_carrito'] = 0
            context['stock_disponible'] = self.object.stock
            
        return context

class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        return Producto.objects.filter(stock__gt=0).order_by('-id')

# Views para vendedores (CRUD de productos)
class VendedorRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario sea vendedor"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_vendedor

class MisProductosView(LoginRequiredMixin, VendedorRequiredMixin, ListView):
    model = Producto
    template_name = 'productos/mis_productos.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        return Producto.objects.filter(
            vendedor=self.request.user.cuentavendedor
        ).order_by('-id')

class CrearProductoView(LoginRequiredMixin, VendedorRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/crear_producto.html'
    success_url = reverse_lazy('productos:mis_productos')
    
    def form_valid(self, form):
        form.instance.vendedor = self.request.user.cuentavendedor
        messages.success(self.request, 'Producto creado exitosamente.')
        return super().form_valid(form)

class EditarProductoView(LoginRequiredMixin, VendedorRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/editar_producto.html'
    success_url = reverse_lazy('productos:mis_productos')
    
    def get_queryset(self):
        # Solo permite editar productos del vendedor actual
        return Producto.objects.filter(vendedor=self.request.user.cuentavendedor)
    
    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)

class EliminarProductoView(LoginRequiredMixin, VendedorRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/eliminar_producto.html'
    success_url = reverse_lazy('productos:mis_productos')
    context_object_name = 'producto'
    
    def get_queryset(self):
        # Solo permite eliminar productos del vendedor actual
        return Producto.objects.filter(vendedor=self.request.user.cuentavendedor)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Producto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# Views para buscar productos por vendedor
class ProductosPorVendedorView(ListView):
    model = Producto
    template_name = 'productos/productos_por_vendedor.html'
    context_object_name = 'productos'
    paginate_by = 12
    
    def get_queryset(self):
        self.vendedor = get_object_or_404(CuentaVendedor, id=self.kwargs['vendedor_id'])
        return Producto.objects.filter(
            vendedor=self.vendedor,
            stock__gt=0
        ).order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendedor'] = self.vendedor
        context['ubicaciones'] = self.vendedor.ubicacionvendedor_set.all()
        return context

# Views para categorías
class ProductosPorCategoriaView(ListView):
    model = Producto
    template_name = 'productos/productos_por_categoria.html'
    context_object_name = 'productos'
    paginate_by = 12
    
    def get_queryset(self):
        self.categoria = self.kwargs['categoria']
        return Producto.objects.filter(
            categoria__iexact=self.categoria,
            stock__gt=0
        ).order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.categoria
        context['total_productos'] = self.get_queryset().count()
        return context

# Views adicionales para funcionalidades específicas
class ActualizarStockView(LoginRequiredMixin, VendedorRequiredMixin, UpdateView):
    model = Producto
    form_class = ActualizarStockForm
    template_name = 'productos/actualizar_stock.html'
    success_url = reverse_lazy('productos:mis_productos')
    
    def get_queryset(self):
        return Producto.objects.filter(vendedor=self.request.user.cuentavendedor)
    
    def form_valid(self, form):
        messages.success(self.request, 'Stock actualizado exitosamente.')
        return super().form_valid(form)

class ActualizarImagenView(LoginRequiredMixin, VendedorRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoImagenForm
    template_name = 'productos/actualizar_imagen.html'
    success_url = reverse_lazy('productos:mis_productos')
    
    def get_queryset(self):
        return Producto.objects.filter(vendedor=self.request.user.cuentavendedor)
    
    def form_valid(self, form):
        messages.success(self.request, 'Imagen actualizada exitosamente.')
        return super().form_valid(form)

def home(request):
    return render(request, "productos/home.html")

def nosotros(request):
    return render(request, "productos/nosotros.html")