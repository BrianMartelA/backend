from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User, Producto, Carrito, ItemCarrito, ItemOrden, Orden
from django.utils.timezone import localtime
import re


ALLOWED_DOMAINS = ['gmail.com', 'duoc.cl', 'yahoo.com']

class RegisterSerializer(serializers.ModelSerializer):
    conf_pass = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
             "first_name", "last_name", "second_last_name",
            "rut", "email", "phone", "address", "password","conf_pass"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_first_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value.strip()

    def validate_last_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El apellido paterno es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El apellido paterno solo puede contener letras y espacios.")
        return value.strip()

    def validate_second_last_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El apellido materno es obligatorio.")
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise serializers.ValidationError("El apellido materno solo puede contener letras y espacios.")
        return value.strip()

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El email es obligatorio.")
        
        # Verificar si el email ya existe
        if User.objects.filter(email=value.strip()).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        
        domain = value.split('@')[-1]
        if domain not in ALLOWED_DOMAINS:
            raise serializers.ValidationError("Solo se permiten correos de Gmail, Duoc o Yahoo.")
        return value.strip()

    def validate_rut(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El RUT es obligatorio.")
        # Chilean RUT validation (basic)
        if not re.match(r'^\d{7,8}-[kK\d]$', value):
            raise serializers.ValidationError("El RUT debe tener el formato 12345678-9 o 12345678-K.")
        if User.objects.filter(rut=value).exists():
            raise serializers.ValidationError("Este RUT ya está registrado.")
        return value.strip()

    def validate_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El teléfono es obligatorio.")
        # Only digits, length between 9 and 12
        if not re.match(r'^\d{9,12}$', value):
            raise serializers.ValidationError("El teléfono debe contener solo números y tener entre 9 y 12 dígitos.")
        return value.strip()

    def validate_address(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La dirección es obligatoria.")
        return value.strip()

    def validate_password(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La contraseña es obligatoria.")
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Debe incluir al menos una letra mayúscula.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Debe incluir al menos un número.")
        if not re.search(r'[\W_]', value):
            raise serializers.ValidationError("Debe incluir al menos un símbolo (como @, #, !).")
        return value

    def validate_conf_pass(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La confirmación de contraseña es obligatoria.")
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']  # Usa email como username
        validated_data.pop('conf_pass')  # Elimina el campo no necesario para crear el usuario
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user



class ProductoSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 
                  'stock', 'imagen', 'imagen_url', 
                  'precio', 'creado_por', 'fecha_creacion',
                  'descripcion']
        extra_kwargs = {
            'creado_por': {'read_only': True},
            'imagen': {'write_only': True}  # Para que no se muestre en las respuestas
        }
    
    def get_imagen(self, obj):
        request = self.context.get('request')
        if obj.imagen:
            return request.build_absolute_uri(obj.imagen.url) if request else obj.imagen.url
        return None
    
    def create(self, validated_data):
        # Asigna automáticamente el usuario actual como creador
        validated_data['creado_por'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen.url)
            return f"http://localhost:8000{obj.imagen.url}"
        return None

class UserManagementSerializer(serializers.ModelSerializer):
    tipo_usuario = serializers.SerializerMethodField()
    fecha_ingreso = serializers.SerializerMethodField()
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'tipo_usuario', 'nombre_completo',
            'fecha_ingreso', 'email', 'rut', 'phone'
        ]

    def get_tipo_usuario(self, obj):
        return "Administrador" if obj.is_staff else "Cliente"

    def get_nombre_completo(self, obj):
        names = [obj.first_name, obj.last_name, obj.second_last_name]
        return " ".join(filter(None, names)) or "Sin nombre"

    def get_fecha_ingreso(self, obj):
        return localtime(obj.date_joined).strftime("%d/%m/%Y %H:%M")

class EmailAuthTokenSerializer(AuthTokenSerializer):
        username = serializers.EmailField(label="Email")

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad', 'fecha_agregado']

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Carrito
        fields = ['id', 'usuario', 'fecha_creacion', 'activo', 'items', 'total']

    def get_total(self, obj):
        return sum(item.producto.precio * item.cantidad for item in obj.items.all())

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "second_last_name",
            "email", "phone", "address"
        ]
        extra_kwargs = {
            "rut": {"read_only": True},
            "email": {"required": False}
        }
    
    def validate_email(self, value):
        # Validar que el email no esté en uso
        if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value
    
    def update(self, instance, validated_data):
        # Actualizar username junto con email
        if 'email' in validated_data:
            validated_data['username'] = validated_data['email']
        return super().update(instance, validated_data)
    
    def validate_phone(self, value):
        if not re.match(r'^\d{9,12}$', value):
            raise serializers.ValidationError("El teléfono debe contener solo números y tener entre 9 y 12 dígitos.")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserProfileSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'second_last_name',
            'rut', 'email', 'phone', 'address', 'nombre_completo'
        ]
    
    def get_nombre_completo(self, obj):
        names = [obj.first_name, obj.last_name, obj.second_last_name]
        return " ".join(filter(None, names)) or "Sin nombre"

class ItemOrdenSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    
    class Meta:
        model = ItemOrden
        fields = ['producto', 'cantidad', 'precio_unitario']

class OrdenSerializer(serializers.ModelSerializer):
    items = ItemOrdenSerializer(many=True, read_only=True)
    
    class Meta:
        model = Orden
        fields = ['id', 'fecha_creacion', 'total', 'items']