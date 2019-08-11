from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRODUCTO_CLASES = (
    ('Eq', 'Equipo'),
    ('Es', 'Esencia'),
    ('R', 'Accesorios'),
)

PRODUCTO_CLASES_DICT = dict(PRODUCTO_CLASES)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    celular = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre

class Color(models.Model):
    color = models.CharField(max_length=20)
    
    def __str__(self):
        return self.color

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    precio = models.FloatField()
    foto = models.ImageField(upload_to='productos/', blank=True)
    marca = models.CharField(max_length=50)
    clase = models.CharField(max_length=50,choices=PRODUCTO_CLASES)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    nicotina = models.BooleanField(blank=True, null=True)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.color:
            return self.producto.nombre + " " + self.color.color
        else:
            return self.producto.nombre

class VentaStock(models.Model):
    producto = models.ForeignKey(Stock, on_delete=models.CASCADE)
    cantidad_compra = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.producto)

class Venta(models.Model):
    productos = models.ManyToManyField(VentaStock)
    total = models.FloatField()
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Venta del %s" % str(self.fecha)


class Caja(models.Model):
    bolivares = models.FloatField(default=0)
    efectivo = models.FloatField(default=0)
    cash = models.FloatField(default=0)
    bofa = models.FloatField(default=0)
    uphold = models.FloatField(default=0)
    cambio_dolar = models.FloatField(default=1)
    
    def __str__(self):
        return "Caja"

class ProductoPedido(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.FloatField(default=0)
    descripcion = models.CharField(max_length=100, blank=True)

class Pedido(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    imagen = models.ImageField(upload_to='pedidos/', blank=True)
    descripcion = models.CharField(max_length=200)
    total = models.FloatField(default=0)
    productos = models.ManyToManyField(ProductoPedido)
    def __str__(self):
        return 'Pedido del %s' % str(self.fecha)
