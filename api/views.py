from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import UserManagementSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from api.models import User

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)  # 👈 Esto muestra los errores en la consola
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
#@permission_classes([IsAdminUser])
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    serializer = UserManagementSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
#@permission_classes([IsAdminUser])
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