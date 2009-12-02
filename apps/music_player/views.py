"""
Views for Music Player interface.
"""
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.forms import ModelForm
from django_jukebox.apps.music_db.models import Song
from django_jukebox.apps.music_player.models import SongRequest

def music_player_main(request):
    """
    Main view for the music player.
    """
    pagevars = {
        "page_title": "Django JukeBox Beta",
    }

    context_instance = RequestContext(request)
    return render_to_response('index.html', pagevars, context_instance)

def display_song_queue(request):
    """
    Display the song queue. Previously played, currently playing, upcoming
    user requests, then upcoming random requests.
    """
    pass