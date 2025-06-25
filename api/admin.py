from django.contrib import admin
from .models import User, Producto  # importa tu modelo personalizado

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'rut','password')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut')
    
#Cristian añadio esta clase
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'stock', 'precio', 'creado_por')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
