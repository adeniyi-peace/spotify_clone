from django.shortcuts import render
from django.views import View

# import modules that will enable background task and scheduling
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone

from .spotify_hompage_webscraper import spotify_webscrapper
from .models import ScrappedData

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


