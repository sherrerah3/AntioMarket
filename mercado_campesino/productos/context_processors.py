"""
Context processors para hacer disponibles variables globales en templates
"""
from django.utils.translation import get_language
from .currency_service import CurrencyService


def currency_context(request):
    """
    Añade información de moneda según el idioma actual
    Español -> COP (Pesos colombianos)
    Inglés -> USD (Dólares)
    """
    current_language = get_language()
    
    # Determinar moneda según idioma
    currency = 'USD' if current_language == 'en' else 'COP'
    
    return {
        'CURRENT_CURRENCY': currency,
        'CURRENCY_SYMBOL': CurrencyService.get_currency_symbol(currency),
        'currency_service': CurrencyService,
    }
