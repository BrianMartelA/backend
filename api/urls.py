from django.urls import path, include
from .views import hello_world, RegisterView, ProductoViewSet, mis_productos #Cristian toco esto
from rest_framework.routers import DefaultRouter #Cristian toco esto

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('hello/', hello_world),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('productos/mis-productos/', mis_productos, name='mis_productos'),
    path('', include(router.urls)),
]
