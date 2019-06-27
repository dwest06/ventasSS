from django.contrib import admin
from .models import Proveedor, Color, Producto, Stock, Venta, Caja

# Register your models here.

admin.site.register(Proveedor)
admin.site.register(Color)
admin.site.register(Producto)
admin.site.register(Stock)
admin.site.register(Venta)
admin.site.register(Caja)
