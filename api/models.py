from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    second_last_name = models.CharField(max_length=150, blank=True)
    
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'rut']
    def __str__(self):
        return self.email

#Cristian creo esta clase
class Producto(models.Model):
    CATEGORIAS = [
        ('HERRAMIENTAS', 'Herramientas'),
        ('ELECTRICOS', 'Materiales Eléctricos'),
        ('FONTANERIA', 'Fontanería'),
        ('CONSTRUCCION', 'Materiales de Construcción'),
    ]
    
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='productos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def imagen_url(self):
        if self.imagen:
            return self.imagen.url
        return None

    def __str__(self):
        return self.nombre
      
    @property
    def descripcion_o_espacio(self):
        return self.descripcion if self.descripcion else "---"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Carrito de {self.usuario.email}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('carrito', 'producto')  # Evita duplicados

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.email}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Orden #{self.orden.id})"
