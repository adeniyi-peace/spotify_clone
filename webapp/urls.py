from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login),
    path("sign-up", views.SignUp.as_view(), name="sign_up"),
    path("artist-profile", views.ArstistProfile.as_view(), name="artist_profile"),
    path("search", views.search),
    path("album", views.AlbumView.as_view(), name="album")
]
