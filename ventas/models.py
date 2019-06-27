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

class Color(models.Model):
    color = models.CharField(max_length=20)
    
    def __str__(self):
        return self.color

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    foto = models.ImageField(upload_to='productos/', blank=True)
    marca = models.CharField(max_length=50)
    clase = models.CharField(max_length=50,choices=PRODUCTO_CLASES)
    proveedor = models.ManyToManyField(Proveedor)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True)
    cantidad = models.PositiveIntegerField(default=0)

class Venta(models.Model):
    productos = models.ManyToManyField(Stock)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "Venta del %s" % str(self.fecha)


class Caja(models.Model):
    bolivares = models.DecimalField(max_digits=5, decimal_places=2)
    efectivo = models.DecimalField(max_digits=5, decimal_places=2)
    cash = models.DecimalField(max_digits=5, decimal_places=2)
    bofa = models.DecimalField(max_digits=5, decimal_places=2)
    uphold = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return "Caja del %s" % str(self.fecha)
    