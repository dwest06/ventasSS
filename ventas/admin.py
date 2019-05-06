from django.contrib import admin
from .models import Producto, Venta, Proveedor

# Register your models here.

admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(Proveedor)