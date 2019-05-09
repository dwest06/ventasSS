from django.urls import path
from .views import *

app_name = 'ventas'

urlpatterns = [
    path('', index, name="index"),
    path('ventas/', resumen_ventas, name="resumen-ventas"),
    path('ventas/obtener-productos', obtener_productos, name="obtener-productos")
]
