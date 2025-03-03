from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("sign-up", views.SignUp.as_view(), name="sign_up"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("search", views.SearchView.as_view(), name="search"),
    path("addremove", views.AddRemoveFollowed.as_view(), name="addremove"),
    path("artist-profile/<str:id>/", views.ArstistProfile.as_view(), name="artist_profile"),
    path("album/<str:id>/", views.AlbumView.as_view(), name="album"),
    path("music/<str:id>/", views.PlaySongView.as_view(), name="song")
]
