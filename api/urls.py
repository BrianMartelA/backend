from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Cambiado de 'auth/register/'
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', delete_user, name='delete-user'),
]
