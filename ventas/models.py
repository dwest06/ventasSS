from django.db import models


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

class Venta(models.Model):
    productos = models.ManyToManyField(Producto)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return "Venta del %s" % str(self.fecha)


