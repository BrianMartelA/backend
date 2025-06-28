from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RegisterSerializer, ProductoSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from .serializers import UserManagementSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from api.models import User
from rest_framework.authtoken.models import Token
from .models import User
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer 
from .permissions import IsAdminUser as IsAdminUserCustom 
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

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

#Cristian toco esto

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

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
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def mis_productos(request):
    productos = Producto.objects.filter(creado_por=request.user)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def prod(request):
    queryset = Producto.objects.all()
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

