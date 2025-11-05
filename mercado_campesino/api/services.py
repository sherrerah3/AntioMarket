"""
Servicio para consumir APIs externas de productos aliados
"""
import requests
from django.core.cache import cache
from typing import Dict, List, Optional


class ProductosAliadosService:
    """Servicio para obtener productos de tiendas aliadas"""
    
    # API del equipo aliado
    API_URL = "https://comercia-1.onrender.com/es/api/products/"
    CACHE_KEY = "productos_aliados_comercia"
    CACHE_TIMEOUT = 1800  # 30 minutos
    
    @staticmethod
    def obtener_productos(cache_enabled=True) -> Dict:
        """
        Obtiene la lista de productos desde la API externa
        
        Args:
            cache_enabled: Si True, usa cache. Si False, hace request directo.
            
        Returns:
            Dict con 'success', 'data' (lista de productos), 'count' y 'error' si falla
        """
        # Intentar obtener del cache primero
        if cache_enabled:
            cached_data = cache.get(ProductosAliadosService.CACHE_KEY)
            if cached_data:
                return {
                    'success': True,
                    'data': cached_data,
                    'count': len(cached_data),
                    'source': 'cache'
                }
        
        try:
            response = requests.get(
                ProductosAliadosService.API_URL,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            productos = data.get('results', [])
            count = data.get('count', len(productos))
            
            # Guardar en cache
            if cache_enabled:
                cache.set(
                    ProductosAliadosService.CACHE_KEY,
                    productos,
                    ProductosAliadosService.CACHE_TIMEOUT
                )
            
            return {
                'success': True,
                'data': productos,
                'count': count,
                'source': 'api'
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'La API externa no respondió a tiempo. Intenta nuevamente.',
                'data': [],
                'count': 0
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'No se pudo conectar con la tienda aliada. Verifica tu conexión.',
                'data': [],
                'count': 0
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Error al consultar productos aliados: {str(e)}',
                'data': [],
                'count': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}',
                'data': [],
                'count': 0
            }
    
    @staticmethod
    def buscar_productos(query: str = None, categoria: Optional[str] = None) -> List[Dict]:
        """
        Busca productos por nombre o categoría
        
        Args:
            query: Término de búsqueda (opcional)
            categoria: Filtrar por categoría específica (opcional)
            
        Returns:
            Lista de productos filtrados
        """
        result = ProductosAliadosService.obtener_productos()
        
        if not result['success']:
            return []
        
        productos = result['data']
        
        # Filtrar por búsqueda
        if query:
            productos = [
                p for p in productos
                if query.lower() in p.get('name', '').lower()
            ]
        
        # Filtrar por categoría
        if categoria and categoria != 'todas':
            productos = [
                p for p in productos
                if p.get('category', '').lower() == categoria.lower()
            ]
        
        return productos
    
    @staticmethod
    def obtener_categorias() -> List[str]:
        """
        Obtiene la lista de categorías únicas disponibles
        
        Returns:
            Lista de nombres de categorías
        """
        result = ProductosAliadosService.obtener_productos()
        
        if not result['success']:
            return []
        
        categorias = set()
        for producto in result['data']:
            if producto.get('category'):
                categorias.add(producto['category'])
        
        return sorted(list(categorias))
    
    @staticmethod
    def limpiar_cache():
        """Limpia el cache de productos aliados"""
        cache.delete(ProductosAliadosService.CACHE_KEY)
        return True
