from django.contrib import admin
from .models import Usuario, CuentaCliente, CuentaVendedor, UbicacionVendedor

# Register your models here.
admin.site.register(Usuario)
admin.site.register(CuentaCliente)
admin.site.register(CuentaVendedor)
admin.site.register(UbicacionVendedor)
