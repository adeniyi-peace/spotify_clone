from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "webapp/homepage.html")

def login(request):
    return render(request, "webapp/login.html")

def register(request):
    return render(request, "webapp/register.html")

def artist_profile(request):
    return render(request, "webapp/artist_profile.html")

def search(request):
    return render(request, "webapp/search.html")

def album(request):
    return render(request, "webapp/album.html")