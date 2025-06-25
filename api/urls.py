from django.urls import path
from .views import hello_world
from .views import RegisterView

urlpatterns = [
    path('hello/', hello_world),
    path('auth/register/', RegisterView.as_view(), name='register'),

]
