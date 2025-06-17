from django.contrib import admin
from .models import User  # importa tu modelo personalizado

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'rut')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'rut')
