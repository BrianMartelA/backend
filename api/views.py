from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view

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