from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    DOB = models.DateField()
    email = models.EmailField(unique=True, max_length=254)
    username = None
    password2 = None

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set', 
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set', 
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.username

class ScrappedData(models.Model):
    artists = models.JSONField(default=list)
    albums = models.JSONField(default=list)