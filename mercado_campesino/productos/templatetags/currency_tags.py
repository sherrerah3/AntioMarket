"""
Template tags y filtros personalizados para conversión de moneda
"""
from django import template
from django.utils.translation import get_language
from productos.currency_service import CurrencyService

register = template.Library()


@register.filter(name='convert_currency')
def convert_currency(price, target_currency=None):
    """
    Convierte un precio de COP a la moneda objetivo
    Uso: {{ producto.precio|convert_currency:CURRENT_CURRENCY }}
    """
    if not target_currency:
        # Determinar moneda por idioma
        current_language = get_language()
        target_currency = 'USD' if current_language == 'en' else 'COP'
    
    return CurrencyService.convert_price(price, target_currency)


@register.filter(name='format_price')
def format_price(price, currency_code=None):
    """
    Formatea un precio con el símbolo de moneda
    Uso: {{ producto.precio|format_price:CURRENT_CURRENCY }}
    """
    if not currency_code:
        # Determinar moneda por idioma
        current_language = get_language()
        currency_code = 'USD' if current_language == 'en' else 'COP'
    
    return CurrencyService.format_price(price, currency_code)


@register.simple_tag
def display_price(price, currency_code=None):
    """
    Convierte y formatea un precio en un solo paso
    Uso: {% display_price producto.precio CURRENT_CURRENCY %}
    """
    if not currency_code:
        # Determinar moneda por idioma
        current_language = get_language()
        currency_code = 'USD' if current_language == 'en' else 'COP'
    
    converted = CurrencyService.convert_price(price, currency_code)
    return CurrencyService.format_price(converted, currency_code)
