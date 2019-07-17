from django.urls import path
from .views import *

app_name = 'ventas'

urlpatterns = [
    path('', index, name="index"),
    path('ventas/', resumen_ventas, name="resumen-ventas"),
    path('ventas/obtener-productos', obtener_productos, name="obtener-productos"),
    path('ventas/obtener-producto-info', obtener_producto_info, name="obtener-producto-info"),
    path('ventas/realizar-venta', realizar_venta, name="realizar-venta"),
    path('caja', caja_info, name="caja"),
    path('proveedores', proveedores, name="proveedores"),
    path('proveedores/add', proveedores_add, name="proveedores-add"),
    path('proveedores/editar/<int:pk>', proveedores_editar, name="proveedores-editar"),
    path('proveedor/delete', proveedor_delete, name="proveedor-delete")
]
