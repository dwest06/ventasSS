""" Vistas de la app """
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.forms import LoginForm
from django.core import serializers
from decimal import Decimal
from .models import *
from .forms import *


from pprint import pprint

# Create your views here.

@login_required
def index(request):
    
    return render(request, 'index.html')

@login_required
def resumen_ventas(request):
    ventas = Venta.objects.all().order_by('-pk')
    pprint(list(ventas))
    context = {
        'ventas' : ventas,
        'ventas_total' : Venta.objects.all().count()
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
        productos = []
        venta = Venta.objects.get(pk=pk)
        for i in venta.productos.all():
            productos.append(str(i))
        print(productos)
        data = {
            "productos" : productos
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
        producto = Stock.objects.get(pk=pk)
        data = {
            'precio' : producto.producto.precio,
            'disponible' : producto.cantidad
        }
        return JsonResponse(data)


@login_required
def realizar_venta(request):
    """
    Metodo para realizar una Venta.
        GET: Muestra los productos que estan disponibles
        POST: Realiza la venta con los productos seleccionados, 
            ademas de actualizar los montos de caja
    """
    if request.method == 'GET':
        productos = Stock.objects.exclude(cantidad = 0)
        
        context = {
            'caja' : Caja.objects.all().first(),
            'productos' : productos
        }
        return render(request, 'ventas/realizar-venta.html', context)
    else:
        stocks = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        fecha = request.POST.get('datetime')
        bolivares = request.POST.get('bolivares')
        efectivo = request.POST.get('efectivo')
        cash = request.POST.get('cash')
        zelle = request.POST.get('zelle')
        uphold = request.POST.get('uphold')
        dolar = request.POST.get('Dolar')

        # Procesamos la venta para ser registrada
        total = 0.0
        venta = Venta.objects.create(total=0,fecha=fecha, vendedor=request.user)
        # Agregamos la Venta
        for i,j in zip(stocks, cantidades):
            stock = Stock.objects.get(pk = i)
            stock.cantidad -= int(j)
            total += float(stock.producto.precio) * float(j)
            venta.productos.add(stock)
            stock.save()
        venta.total = total
        venta.save()

        # Procesamos la Caja
        caja = Caja.objects.all().first()
        caja.bolivares += float(bolivares)
        caja.efectivo += float(efectivo)
        caja.cash += float(cash)
        caja.bofa += float(zelle)
        caja.uphold += float(uphold)
        if dolar:
            caja.cambio_dolar = float(dolar)
        caja.save()

        messages.success(request, "Venta registrada exitosamente")
        return redirect('ventas:realizar-venta')

"""
    
    SECCION DE MANEJO DE CAJA

"""
@login_required
def caja_info(request, *args, **kwargs):
    """
    Metodo para ver info de Caja
        GET: Ver info de Caja
        POST: Mover dinero de un activo a otro
    """
        
    if request.method == "GET":
        caja = Caja.objects.all().first()
        total = (caja.bolivares / caja.cambio_dolar) + (caja.efectivo * caja.cambio_dolar)
        total += caja.bofa + caja.cash + caja.uphold
        return render(request, 'caja/caja.html', {'caja' : caja, 'total' : round(total,2) })
    else:
        accion = request.POST.get('tipo')
        caja = Caja.objects.all().first()
        
        def egresar_de(de, cantidad):
            if de == 'bolivares':
                caja.bolivares -= float(cantidad)
            elif de == 'efectivo':
                caja.efectivo -= float(cantidad)
            elif de == 'bofa':
                caja.bofa -= float(cantidad)
            elif de == 'cash':
                caja.cash -= float(cantidad)
            elif de == 'uphold':
                caja.uphold -= float(cantidad)
        def ingresar_para(para, cantidad):
            if para == 'bolivares':
                caja.bolivares += float(cantidad)
            elif para == 'efectivo':
                caja.efectivo += float(cantidad)
            elif para == 'bofa':
                caja.bofa += float(cantidad)
            elif para == 'cash':
                caja.cash += float(cantidad)
            elif para == 'uphold':
                caja.uphold += float(cantidad)
        
        if accion == "movimiento":
            de = request.POST.get('cambioDe')
            para = request.POST.get('cambioPara')
            cantidad = request.POST.get('cantidad')
            dolar = request.POST.get('valorDolar')
            print(de, para, cantidad)
            # Realizamo el cambio de una moneda a otra
            if de == 'bolivares' or de == 'efectivo':
                dolares = float(cantidad) * float(dolar)
                egresar_de(de, cantidad)
                ingresar_para(para, dolares)
            else:
                egresar_de(de, cantidad)
                ingresar_para(para, cantidad)
            caja.save()
                
        else:
            de = request.POST.get('egresoDe')
            cantidad = request.POST.get('cantidad')
            dolar = request.POST.get('valorDolar')
            if de == 'bolivares' or de == 'efectivo':
                egresar_de(de, cantidad)
            else:
                egresar_de(de, cantidad)
            caja.save()

    messages.success(request, "Cambio realizado Exitosamente")
    return redirect('ventas:caja')


"""

    CRUD DE PROVEEDORES

"""

@login_required
def proveedores(request, *args, **kwargs):
    if request.method == 'GET':
        proveedores = Proveedor.objects.all()
        return render(request, 'proveedores/proveedores.html', {'proveedores' : proveedores})

@login_required
def proveedores_add(request, *args, **kwargs):
    if request.method == 'GET':
        form = ProveedorForm()
        return render(request, 'proveedores/proveedores-add.html', {'form': form})
    else:
        form = ProveedorForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()

        return redirect('ventas:proveedores')

@login_required
def proveedores_editar(request, *args, **kwargs):
    if request.method =='GET':
        print(args, kwargs)
        form = ProveedorForm()
        return render(request, 'proveedores/proveedores-add.html', {'form': form})
    else:
        pass

@login_required
def proveedor_delete(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST.get('proveedor')
        proveedor = Proveedor.objects.get(pk=pk)
        nombre = proveedor.nombre
        proveedor.delete()
        messages.success(request,'Proveedor ' + nombre + ' eliminado exitosamente' )
        return redirect('ventas:proveedores')