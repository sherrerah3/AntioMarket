from django.http import JsonResponse
from django.conf import settings
from productos.models import Producto

def productos_disponibles(request):
    """Devuelve la lista de productos con stock > 0 en formato JSON."""
    base_url = "http://54.158.38.201"

    productos_queryset = Producto.objects.filter(stock__gt=0).values('id', 'nombre', 'stock')

    productos = []
    for p in productos_queryset:
        productos.append({
            'id': p['id'],
            'nombre': p['nombre'],
            'stock': p['stock'],
            'url': f"{base_url}/producto/{p['id']}/"
        })

    return JsonResponse(productos, safe=False)
