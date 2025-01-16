from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "homepage.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def artist_profile(request):
    return render(request, "artist_profile.html")

def search(request):
    return render(request, "search.html")