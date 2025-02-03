from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from .managers import CustomUserManger

# Create your models here.

class CustomUser(AbstractUser):
    DOB = models.DateField(null=True)
    email = models.EmailField(unique=True, max_length=254)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManger()

    def __str__(self):
        return self.email
    
    

class ScrappedData(models.Model):
    artists = models.JSONField(default=list)
    albums = models.JSONField(default=list)