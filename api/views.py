from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RegisterSerializer, ProductoSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .serializers import UserManagementSerializer, CarritoSerializer, ItemCarritoSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes, action
from api.models import User
from rest_framework.authtoken.models import Token
from .models import User, Carrito, ItemCarrito
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer 
from .permissions import IsAdminUser as IsAdminUserCustom 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

#Cristian toco esto
from .models import Producto
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class CustomAuthTokenSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        # Permitir login con email como username
        email = attrs.get('email')
        if email:
            attrs['username'] = email
        return super().validate(attrs)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)  # 👈 Esto muestra los errores en la consola
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Alvaro toco esto

class ProductPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def all_products(request):
    productos = Producto.objects.all()
    # Pasar el contexto de la solicitud al serializador
    serializer = ProductoSerializer(productos, many=True, context={'request': request})
    return Response(serializer.data)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'categoria', 'descripcion']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context




class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff  # Añade esta propiedad
            }
        })
    
class UserPagination(PageNumberPagination):
    page_size = 6  # Cambiado a 6 usuarios por página
    page_size_query_param = 'page_size'
    max_page_size = 100



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_productos(request):
    productos = Producto.objects.filter(creado_por=request.user)
    # Pasar el contexto de la solicitud al serializador
    serializer = ProductoSerializer(productos, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def prod(request):
    queryset = Producto.objects.all()
    serializer = ProductoSerializer(
        queryset, 
        many=True, 
        context={'request': request}  # Pasa el contexto
    )
    serializer_class = ProductoSerializer(queryset, many=True, context={'request': request})
    return Response(serializer_class.data)

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hola desde Django!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_list(request):
    search_query = request.query_params.get('search', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(rut__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    paginator = UserPagination()
    paginated_users = paginator.paginate_queryset(users, request)
    
    serializer = UserManagementSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    serializer = CarritoSerializer(carrito)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_item_carrito(request):
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)
    
    try:
        producto = Producto.objects.get(pk=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user, activo=True)
    
    item, item_created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': cantidad}
    )
    
    if not item_created:
        item.cantidad += int(cantidad)
        item.save()
    
    serializer = ItemCarritoSerializer(item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_item_carrito(request, item_id):
    try:
        item = ItemCarrito.objects.get(pk=item_id, carrito__usuario=request.user)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ItemCarrito.DoesNotExist:
        return Response({'error': 'Item no encontrado'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def toggle_admin_status(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"error": "Usuario no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # No permitir modificar superusuarios
    if user.is_superuser:
        return Response(
            {"error": "No se puede modificar un superusuario"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # No permitir que un admin se quite sus propios permisos
    if user.id == request.user.id:
        return Response(
            {"error": "No puedes cambiar tu propio estado de administrador"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Cambiar el estado de is_staff
        user.is_staff = not user.is_staff
        user.save()
        
        return Response(
            {"message": f"Usuario {'ahora es administrador' if user.is_staff else 'ya no es administrador'}"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

