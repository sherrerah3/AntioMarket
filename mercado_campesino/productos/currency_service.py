"""
Servicio para conversión de moneda usando ExchangeRate-API
"""
import requests
from decimal import Decimal
from django.core.cache import cache
from django.conf import settings


class CurrencyService:
    """Servicio para obtener tasas de cambio y convertir monedas"""
    
    BASE_URL = "https://api.exchangerate-api.com/v4/latest/COP"
    CACHE_TIMEOUT = 3600  # 1 hora en segundos
    
    @staticmethod
    def get_exchange_rates():
        """
        Obtiene las tasas de cambio desde la API o cache
        Returns: dict con tasas de cambio o None si falla
        """
        # Intentar obtener del cache primero
        rates = cache.get('exchange_rates')
        if rates:
            return rates
        
        try:
            response = requests.get(CurrencyService.BASE_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            rates = data.get('rates', {})
            
            # Guardar en cache
            cache.set('exchange_rates', rates, CurrencyService.CACHE_TIMEOUT)
            return rates
        except Exception as e:
            print(f"Error obteniendo tasas de cambio: {e}")
            # Tasas de respaldo en caso de error
            return {
                'USD': 0.00025,  # Aproximado: 1 COP = 0.00025 USD
                'EUR': 0.00023,  # Aproximado: 1 COP = 0.00023 EUR
                'COP': 1.0
            }
    
    @staticmethod
    def convert_price(price_cop, target_currency='USD'):
        """
        Convierte un precio de COP a otra moneda
        
        Args:
            price_cop: Precio en pesos colombianos (Decimal o float)
            target_currency: Moneda objetivo (USD, EUR, etc.)
            
        Returns:
            Decimal: Precio convertido
        """
        if target_currency == 'COP':
            return Decimal(str(price_cop))
        
        rates = CurrencyService.get_exchange_rates()
        if not rates or target_currency not in rates:
            return Decimal(str(price_cop))
        
        rate = Decimal(str(rates[target_currency]))
        converted = Decimal(str(price_cop)) * rate
        
        return converted.quantize(Decimal('0.01'))  # Redondear a 2 decimales
    
    @staticmethod
    def get_currency_symbol(currency_code):
        """
        Retorna el símbolo de la moneda
        
        Args:
            currency_code: Código de moneda (USD, EUR, COP)
            
        Returns:
            str: Símbolo de la moneda
        """
        symbols = {
            'COP': '$',
            'USD': 'US$',
            'EUR': '€',
            'GBP': '£'
        }
        return symbols.get(currency_code, currency_code)
    
    @staticmethod
    def format_price(price, currency_code):
        """
        Formatea un precio con su símbolo de moneda
        
        Args:
            price: Precio a formatear
            currency_code: Código de moneda
            
        Returns:
            str: Precio formateado con símbolo
        """
        symbol = CurrencyService.get_currency_symbol(currency_code)
        price_decimal = Decimal(str(price))
        
        if currency_code == 'COP':
            # Sin decimales para pesos colombianos
            return f"{symbol}{price_decimal:,.0f}".replace(',', '.')
        else:
            # Con 2 decimales para otras monedas
            return f"{symbol}{price_decimal:,.2f}"
