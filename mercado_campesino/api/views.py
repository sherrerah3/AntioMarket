from django.http import JsonResponse
from django.conf import settings
from productos.models import Producto
from .services import ProductosAliadosService

def productos_disponibles(request):
    """Devuelve la lista de productos con stock > 0 en formato JSON."""
    base_url = "http://54.158.38.201/"

    productos_queryset = Producto.objects.filter(stock__gt=0).values('id', 'nombre', 'stock')

    productos = []
    for p in productos_queryset:
        productos.append({
            'id': p['id'],
            'nombre': p['nombre'],
            'stock': p['stock'],
            'url': f"{base_url}producto/{p['id']}/"
        })

    return JsonResponse(productos, safe=False)


def productos_aliados(request):
    """API que devuelve productos de tiendas aliadas en formato JSON"""
    
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.GET.get('buscar', '').strip()
    categoria = request.GET.get('categoria', '')
    
    # Obtener productos desde la API externa
    if busqueda or categoria:
        productos = ProductosAliadosService.buscar_productos(
            query=busqueda if busqueda else None,
            categoria=categoria if categoria else None
        )
        result = {
            'success': True,
            'count': len(productos),
            'results': productos
        }
    else:
        result = ProductosAliadosService.obtener_productos()
        if result['success']:
            result['results'] = result.pop('data')
    
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
