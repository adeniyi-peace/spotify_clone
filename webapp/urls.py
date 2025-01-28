from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login),
    path("register", views.register),
    path("artist-profile", views.artist_profile),
    path("search", views.search),
    path("album", views.album)
]
