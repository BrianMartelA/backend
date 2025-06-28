
from django.urls import path, include
from .views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('hello/', hello_world),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', delete_user, name='delete-user'),
    path('users/<int:pk>/toggle-admin/', toggle_admin_status, name='toggle-admin'),
    path('productos/mis-productos/', mis_productos, name='mis_productos'),
    path('productos/all/', all_products, name='all-products'),  # Nueva ruta
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),  # Esto debe ir AL FINAL
]