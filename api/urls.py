from django.conf.urls.static import static
from django.urls import path, include
from .views import * 
from rest_framework.routers import DefaultRouter 
from django.conf import settings

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
    
    path('carrito/', obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', agregar_item_carrito, name='agregar_item_carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
