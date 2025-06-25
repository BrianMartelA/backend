from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RegisterSerializer, ProductoSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

#Cristian toco esto
from .models import Producto
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)  # 👈 Esto muestra los errores en la consola
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hola desde Django!"})

#Cristian toco esto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mis_productos(request):
    productos = Producto.objects.filter(creado_por=request.user)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)