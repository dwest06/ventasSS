from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.forms import LoginForm
from django.core import serializers
from .models import *
from .forms import *


from pprint import pprint


# Create your views here.

@login_required
def index(request):
    
    return render(request, 'index.html')

@login_required
def resumen_ventas(request):
    context = {
        'ventas' : Venta.objects.all()
    }
    return render(request, 'ventas/ventas-resumen.html', context)

@login_required
def obtener_productos(request, *args, **kwargs):
    """
        Metodo para obtener la lista de los productos 
        vendidos en una venta
    """
    if request.method == "POST":
        pk = request.POST.get('pk')
        a = serializers.serialize("json", list(Venta.objects.get(pk=pk).productos.all()))
        print(a)
        data = {
            "productos" : a
        }
        return JsonResponse(data)

@login_required
def obtener_producto_info(request, *args, **kwargs):
    """ 
        Metodo para obtener la info de un producto
        al momento de realizar una venta
    """
    if request.method == "POST":
        pk = request.POST.get('pk')
        producto = Producto.objects.get(pk=pk)
        complemento = None
        """if producto.clase == 'Eq':
            complemento = producto.color.filter(disponible=True)
        elif producto.clase == 'Es':
           """ 
        
        data = {
            'precio' : producto.precio,
            'complemento' : complemento
        }
        print(producto.precio)
        return JsonResponse(data)


@login_required
def realizar_venta(request):
    if request.method == 'GET':
        productos = Producto.objects.all()
        context = {
            'productos' : productos
        }
        return render(request, 'ventas/realizar-venta.html', context)
    else:
        pprint(request.POST)
        messages.success(request, "Venta registrada exitosamente")
        return redirect('ventas:realizar-venta')