
from django.urls import path, include
from .views import * #Cristian toco esto
from rest_framework.routers import DefaultRouter #Cristian toco esto

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('hello/', hello_world),
    path('register/', RegisterView.as_view(), name='register'),  # Cambiado de 'auth/register/'
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', delete_user, name='delete-user'),
    path('productos/mis-productos/', mis_productos, name='mis_productos'),
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('productos/all/',prod,name='productos'),
    path('users/<int:pk>/toggle-admin/', toggle_admin_status, name='toggle-admin')
]
