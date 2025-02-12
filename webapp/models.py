from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManger

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
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

class FollowedArtist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="follow")
    id = models.CharField( max_length=100, unique=True, primary_key=True, db_index=True)
    name = models.CharField( max_length=100)
    image_url = models.URLField( max_length=200)

    def __str__(self):
        return self.name
    