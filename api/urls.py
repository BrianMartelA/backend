from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter 
from django.conf import settings
#from .views import * 
from .views import (  # Cambia a importación explícita
    hello_world,
    RegisterView,
    user_list,
    delete_user,
    toggle_admin_status,
    mis_productos,
    all_products,
    LoginView,
    obtener_carrito,
    agregar_item_carrito,
    eliminar_item_carrito,
    buscar_productos,
    productos_paginados,
    productos_por_categoria,  # 👈 Añade esto explícitamente
    ProductoViewSet,
    CurrentUserView,
    change_password
)


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

    #path('productos/all',prod,name='productos'),
    
    path('carrito/', obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', agregar_item_carrito, name='agregar_item_carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),

    path('productos/search/', buscar_productos, name='search-products'),
    path('productos/paginados/', productos_paginados, name='productos-paginados'),
    path('productos/por-categoria/', productos_por_categoria, name='productos-por-categoria'),

    path('user/me/', CurrentUserView.as_view(), name='current-user'),
    path('user/change_password/', change_password, name='change-password'),

    path('', include(router.urls)),  # Esto debe ir AL FINAL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

