from django.conf import settings 
from django.conf.urls.static import static 

from django.urls import path
from .views import *

app_name = 'ventas'

urlpatterns = [
    path('', index, name="index"),
    # Ventas
    path('ventas/', resumen_ventas, name="resumen-ventas"),
    path('ventas/obtener-productos', obtener_productos, name="obtener-productos"),
    path('ventas/obtener-producto-info', obtener_producto_info, name="obtener-producto-info"),
    path('ventas/realizar-venta', realizar_venta, name="realizar-venta"),
    # Caja
    path('caja', caja_info, name="caja"),
    # Proveedores
    path('proveedores', proveedores, name="proveedores"),
    path('proveedores/add', proveedores_add, name="proveedores-add"),
    path('proveedores/editar/<int:pk>', proveedores_editar, name="proveedores-editar"),
    path('proveedor/delete', proveedor_delete, name="proveedor-delete"),
    # Producto
    path('producto', producto, name="producto"),
    path('producto/add', producto_add, name="producto-add"),
    path('producto/editar/<int:pk>', producto_editar, name="producto-editar"),
    path('producto/delete', producto_delete, name="producto-delete"),
    path('addstock', addstock, name="add-stock"),
    # Stock
    path('stock', stock, name="stock"),
    path('stock/add', stock_add, name="stock-add"),
    path('stock/editar/<int:pk>', stock_editar, name="stock-editar"),
    path('stock/delete', stock_delete, name="stock-delete"),
    # Color
    path('producto/color/add', color_add, name="color-add")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)