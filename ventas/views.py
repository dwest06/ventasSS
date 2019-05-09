from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from usuarios.forms import LoginForm
from django.core import serializers
from .models import *


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
    pk = request.POST.get('pk')
    a = serializers.serialize("json", list(Venta.objects.get(pk=pk).productos.all()))
    print(a)
    data = {
        "productos" : a
    }
    return JsonResponse(data)