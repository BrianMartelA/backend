from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    second_last_name = models.CharField(max_length=150, blank=True)

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
    imagen = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='productos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre