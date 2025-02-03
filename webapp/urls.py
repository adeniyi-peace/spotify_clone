from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login", views.login),
    path("sign-up", views.SignUp.as_view(), name="sign_up"),
    path("artist-profile/<str:id>/", views.ArstistProfile.as_view(), name="artist_profile"),
    path("search", views.SearchView.as_view(), name="search"),
    path("album/<str:id>/", views.AlbumView.as_view(), name="album")
]
