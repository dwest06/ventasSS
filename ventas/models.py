from django.db import models
from django.contrib.auth.models import User

# Create your models here.

PRODUCTO_CLASES = (
    ('Eq', 'Equipo'),
    ('Es', 'Esencia'),
    ('R', 'Resistencia'),
)

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    celular = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='productos/', blank=True)
    marca = models.CharField(max_length=50)
    clase = models.CharField(max_length=50,choices=PRODUCTO_CLASES)
    sabor = models.CharField(max_length=50, blank=True)     # Para las esencias
    color = models.CharField(max_length=50, blank=True)     # Para los equipos
    proveedor = models.ManyToManyField(Proveedor)

    def __str__(self):
        return self.nombre

class ProductoVenta(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __init__(self):
        return self.producto.nombre

class Venta(models.Model):
    productos = models.ManyToManyField(ProductoVenta)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    vendido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Venta del %s" % str(self.fecha)


class Caja(models.Model):
    bolivares = models.DecimalField(max_digits=5, decimal_places=2)
    cash = models.DecimalField(max_digits=5, decimal_places=2)
    bofa = models.DecimalField(max_digits=5, decimal_places=2)
    uphold = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    def __str__(self):
        return "Caja del %s" % str(self.fecha)
    