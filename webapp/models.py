from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# class CustomUser(AbstractUser):
#     email = models.EmailField( max_length=254)

class ScrappedData(models.Model):
    artists = models.JSONField(default=list)
    albums = models.JSONField(default=list)