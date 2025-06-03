from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    second_last_name = models.CharField(max_length=150, blank=True)
