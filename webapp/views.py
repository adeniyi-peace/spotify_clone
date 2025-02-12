from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

import json

# import modules that will enable background task and scheduling
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone

from .spotify_webscraper import spotify_webscrapper, get_artist_details, get_album_details, get_search, search_song
from .models import ScrappedData, FollowedArtist
from .forms import CreateUserForm, LoginUserForm
from .music_context_processor import SongSession

# Create your views here.

# initiliaze schedulers
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)


def scheduled_task():
    pop_artist, pop_albums = spotify_webscrapper()

    scrapper = ScrappedData

    if not scrapper.objects.exists():
        scrapper.objects.create(artists=pop_artist, albums=pop_albums)

    else:
        scrapper.objects.all().update(artists=pop_artist, albums=pop_albums)


class Index(View):
    def get(self, request):
        # Check if the scheduler is already started
        if not scheduler.running:
            scheduler.start()

        # Schedule the task if it's not already scheduled
        if not scheduler.get_job('my_job'):
            scheduler.add_job(
                scheduled_task,
                'interval', 
                hours=3, 
                id='my_job', 
                replace_existing=True, 
                next_run_time=timezone.now(), 
                max_instances=1
            )

        scrapper = ScrappedData.objects.all()[0]

        pop_artist = scrapper.artists
        pop_albums = scrapper.albums

        context = {"pop_artists":pop_artist,
                   "pop_albums":pop_albums}

        return render(request, "webapp/homepage.html", context)
    
    


class LoginView(View):
    def get(self, request):
        form = LoginUserForm()
        context = {"form":form}
        return render(request, "webapp/login.html", context)
    
    def post(self, request):
        form = LoginUserForm(request, request.POST)

        if form.is_valid():
            email = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)
            print(user)

            if user :
                login(request, user)
                return redirect(reverse("index"))

        context = {"form":form}
        return render(request, "webapp/login.html", context)

class SignUp(View):
    def get(self, request):
        form = CreateUserForm()

        context = {"form":form}

        return render(request, "webapp/sign_up.html", context)
    
    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect(reverse("index"))
        
        context = {"form":form}

        return render(request, "webapp/sign_up.html", context)
        


class ArstistProfile(View):
    def get(self, request, id):
        artist_details = get_artist_details(id)
        followed = FollowedArtist.objects.filter(id=id)
        context = {"artist_details":artist_details, "followed":followed}
        return render(request, "webapp/artist_profile.html", context)

    

class AddRemoveFollowed(View):
    def post(self, request):
        id = request.POST.get("id")
        followed = FollowedArtist.objects.filter(id=id)
        previous_page =request.META.get("HTTP_REFERER")

        if followed :
            followed.delete()

        else:
            id = request.POST.get("id")
            artist = request.POST.get("artist")
            image_url = request.POST.get("image_url")
            FollowedArtist.objects.create(user=request.user, id=id, name=artist, image_url =image_url)

        return redirect(previous_page)

class SearchView(View):
    def get(self, request):
        context =request.session.get("search_result", {})
        # if "search_result" in request.session:
        #     del request.session["search_result"]
        return render(request, "webapp/search.html", context)
    
    
    def post(self, request):
        query = request.POST.get("query")
        data = get_search(query)
        albums = data.get("albums")
        tracks = data.get("tracks")
        artists = data.get("artists")
        top_result = data.get("top_result")
        top_tracks = tracks[:4]
        top_albums =albums[:5]
        top_artists = artists[:5]
        context = {"albums":albums, "artists":artists, "tracks":tracks, "top_result":top_result,
                   "top_tracks":top_tracks, "top_albums":top_albums, "top_artists":top_artists}
        request.session["search_result"] = context
        return render(request, "webapp/search.html", context)

class AlbumView(View):
    def get(self, request, id):
        album_details = get_album_details(id)
        context = {"album_details":album_details}
        return render(request, "webapp/album.html", context)
    

class PlaySongView(View):
    def get(self, request, id):
        previous_page =request.META.get("HTTP_REFERER")

        song = SongSession(request)

        song_details = search_song(id)

        song.save_song(**song_details)

        return redirect(previous_page)
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("index"))


