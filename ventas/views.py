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

"""

    VENTAS

"""

@login_required
def resumen_ventas(request):
    ventas = Venta.objects.all().order_by('-pk')
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
            productos.append(str(i) + ' ...... cant: ' + str(i.cantidad_compra))
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
        # Factura
        stocks = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        fecha = request.POST.get('datetime')
        total = float(request.POST.get('total'))

        # Pago
        bolivares = float(request.POST.get('bolivares'))
        efectivo = float(request.POST.get('efectivo'))
        cash = float(request.POST.get('cash'))
        zelle = float(request.POST.get('zelle'))
        uphold = float(request.POST.get('uphold'))
        dolar = float(request.POST.get('Dolar'))

        # Verificacion de Pago total
        total_pago = cash + zelle + uphold + (bolivares/dolar) + (efectivo/dolar)
        if total > total_pago:
            print('Total: ', total, 'Pago: ', total_pago)
            messages.error(request, "Pago insuficiente.")
            return redirect(request.path_info)
        elif total < total_pago:
            print('Total: ', total, 'Pago: ', total_pago)
            messages.error(request, "Pago mayor al total.")
            return redirect(request.path_info)

        # Procesamos la venta para ser registrada
        total = 0.0
        venta = Venta.objects.create(total=0,fecha=fecha, vendedor=request.user)
        # Agregamos la Venta
        for i,j in zip(stocks, cantidades):
            stock = Stock.objects.get(pk = i)
            ventastock = VentaStock.objects.create(producto=stock, cantidad_compra=j)
            stock.cantidad -= int(j)
            total += float(stock.producto.precio) * float(j)
            venta.productos.add(ventastock)
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
        total = (caja.bolivares / caja.cambio_dolar) + (caja.efectivo / caja.cambio_dolar)
        total += caja.bofa + caja.cash + caja.uphold
        return render(request, 'caja/caja.html', {'caja' : caja, 'total' : round(total,2) })
    else:
        accion = request.POST.get('tipo')
        caja = Caja.objects.all().first()
        
        def egresar_de(de, cantidad):
            if de == 'bolivares':
                caja.bolivares -= cantidad
            elif de == 'efectivo':
                caja.efectivo -= cantidad
            elif de == 'bofa':
                caja.bofa -= cantidad
            elif de == 'cash':
                caja.cash -= cantidad
            elif de == 'uphold':
                caja.uphold -= cantidad
        def ingresar_para(para, cantidad):
            if para == 'bolivares':
                caja.bolivares += cantidad
            elif para == 'efectivo':
                caja.efectivo += cantidad
            elif para == 'bofa':
                caja.bofa += cantidad
            elif para == 'cash':
                caja.cash += cantidad
            elif para == 'uphold':
                caja.uphold += cantidad
        
        if accion == "movimiento":
            de = request.POST.get('cambioDe')
            para = request.POST.get('cambioPara')
            cantidad = float(request.POST.get('cantidad'))
            dolar = float(request.POST.get('valorDolar'))
            print(de, para, cantidad, dolar)

            # Realizamo el cambio de una moneda a otra
            if de == 'bolivares' or de == 'efectivo':
                if para == 'bolivares' or para == 'efectivo':
                    egresar_de(de, cantidad)
                    ingresar_para(para, cantidad)
                else:
                    dolares = cantidad / dolar
                    egresar_de(de, cantidad)
                    ingresar_para(para, dolares)
            else:
                if para == 'bolivares' or para == 'efectivo':
                    dolares = cantidad * dolar
                    egresar_de(de, cantidad)
                    ingresar_para(para, dolares)
                else:
                    egresar_de(de, cantidad)
                    ingresar_para(para, cantidad)
            
            # Si hubo un cambio en el Dolar
            if dolar != caja.cambio_dolar and dolar != None:
                caja.cambio_dolar = dolar

            caja.save()
                
        else:
            de = request.POST.get('egresoDe')
            cantidad = request.POST.get('cantidad')
            dolar = request.POST.get('valorDolar')
            if de == 'bolivares' or de == 'efectivo':
                egresar_de(de, cantidad)
            else:
                egresar_de(de, cantidad)
            
            # Si hubo un cambio en el Dolar
            if dolar != caja.cambio_dolar and dolar != None:
                caja.cambio_dolar = dolar
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
        return render(request, 'proveedores/proveedores.html', {'proveedores' : proveedores, 'proveedores_total' : proveedores.count()})

@login_required
def proveedores_add(request, *args, **kwargs):
    if request.method == 'GET':
        form = ProveedorForm()
        return render(request, 'proveedores/proveedores-add.html', {'form': form})
    else:
        form = ProveedorForm(request.POST)
        print(form)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            form.save()
            messages.success(request, "Producto "+ nombre +" añadido exitosamente")

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

"""

    CRUD DE PRODUCTOS

"""
@login_required
def producto(request, *args, **kwargs):
    if request.method == 'GET':
        filtro = request.GET.get('filtro')
        if filtro:
            producto = Producto.objects.filter(clase = filtro)
        else:
            producto = Producto.objects.all()
        context = {
            'productos' : producto, 
            'producto_total' : producto.count(),
            'clases' : PRODUCTO_CLASES_DICT,
            'filtro' : PRODUCTO_CLASES_DICT.get(filtro)
        }
        return render(request, 'producto/producto.html', context)
    return redirect('ventas:producto')

@login_required
def producto_add(request, *args, **kwargs):
    if request.method == 'GET':
        form = ProductoForm()
        return render(request, 'producto/producto-add.html', {'form': form})
    else:
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha agregado el producto exitosamente")
        else:
            messages.error(request, "No se ha podido agregar el producto")

        return redirect('ventas:producto')

@login_required
def producto_editar(request, *args, **kwargs):

    if request.method =='GET':
        pk = kwargs.get('pk')
        producto = Producto.objects.get(pk=pk)
        form = ProductoForm(instance=producto)
        return render(request, 'producto/producto-add.html', {'form': form, 'editar': True, 'pk': pk})
    else:
        form = ProductoForm(request.POST)
        if form.is_valid():
            
            messages.success(request, "Se ha agregado el producto exitosamente")
        else:
            messages.error(request, "No se ha podido agregar el producto")

        return redirect('ventas:producto')


@login_required
def producto_delete(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST.get('producto')
        producto = Producto.objects.get(pk=pk)
        nombre = str(producto)
        producto.delete()
        messages.success(request,'Porducto ' + nombre + ' eliminado exitosamente' )
    
    return redirect('ventas:producto')

"""

    CRUD DE STOCK

"""

@login_required
def stock(request, *args, **kwargs):
    if request.method == 'GET':
        filtro = request.GET.get('filtro')
        if filtro:
            stock = Stock.objects.filter(producto__clase = filtro)
        else:
            stock = Stock.objects.all()
        context = {
            'productos' : stock, 
            'producto_total' : stock.count(),
            'clases' : PRODUCTO_CLASES_DICT,
            'filtro' : PRODUCTO_CLASES_DICT.get(filtro)
        }
        return render(request, 'stock/stock.html', context)


@login_required
def stock_add(request, *args, **kwargs):
    if request.method == 'GET':
        form = StockForm()
        return render(request, 'stock/stock-add.html', {'form': form})
    else:
        form =StockForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            color = form.cleaned_data['color']
            nicotina = form.cleaned_data['nicotina']

            if producto.clase == 'Es':
                # Verificamos que nicotina no sea null
                if nicotina is None:
                    messages.error(request, "Por favor indique si el producto posee nicotina o no")
                    return redirect(request.path_info)
                
                stock, status = Stock.objects.get_or_create(producto = producto, color = color, nicotina = nicotina)

            else:
                stock, status = Stock.objects.get_or_create(producto = producto, color = color)
            if status:
                stock.cantidad = int(cantidad)
                stock.save()
                messages.success(request, "Se ha agregado el stock exitosamente.")
            else:
                stock.cantidad += int(cantidad)
                stock.save()
                messages.warning(request, "El producto "+ str(stock) +" ya se encuentra agregado. Sin embargo se ha agregado la cantida al stock.")
        else:
            messages.error(request, "No se ha podido agregar el stock")

        return redirect('ventas:stock')

@login_required
def stock_editar(request, *args, **kwargs):
    """
        Editamos el mismo objeto, es decir, no se va a crear uno nuevo
    """
    if request.method =='GET':
        pk = kwargs.get('pk')
        stock = Stock.objects.get(pk=pk)
        pprint(stock.__dict__)
        form = StockForm(instance=stock)
        return render(request, 'stock/stock-add.html', {'form': form, 'editar': True, 'pk': pk})
    else:
        form = StockForm(request.POST)
        if form.is_valid():
            pk = request.POST.get('pk')
            stock = Stock.objects.get(pk=pk)
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            color = form.cleaned_data['color']

            stock.producto = producto
            stock.cantidad = cantidad
            stock.color = color
            stock.save()

            messages.success(request, "Se ha editado el stock exitosamente.")
        else:
            messages.error(request, "No se ha podido editar el stock.")

        return redirect('ventas:stock')


@login_required
def stock_delete(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST.get('stock')
        stock = Stock.objects.get(pk=pk)
        nombre = str(stock)
        stock.delete()
        messages.success(request,'Porducto ' + nombre + ' eliminado exitosamente' )
    
    return redirect('ventas:stock')


@login_required
def addstock(request, *args, **kwargs):
    if request.method == "POST":
        pk = request.POST.get('stock')
        cantidad = request.POST.get('cantidad')
        stock = Stock.objects.get(pk=pk)
        nombre = str(stock)
        stock.cantidad += int(cantidad)
        stock.save()
        messages.success(request, "Stock "+ nombre +" añadido con exito")
    
    return redirect('ventas:producto')

"""

    COLOR

"""

@login_required
def color_add(request, *args, **kwargs):
    if request.method == 'POST':
        nombre = request.POST.get('color')
        c, status = Color.objects.get_or_create(color=nombre)
        if status:
            messages.success(request, "Color " + nombre + " Agregado")
        else:
            messages.warning(request, "El Color "+ nombre +" ya existe")
        return redirect('ventas:stock-add')