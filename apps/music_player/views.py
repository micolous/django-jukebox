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
    currently_playing_track = SongRequest.objects.filter(time_played__isnull=False).order_by('-time_played')[0]
    print currently_playing_track
    recently_played_tracks = SongRequest.objects.filter(time_played__isnull=False).exclude(id=currently_playing_track.id).order_by('-time_played')
    
    # Determine total number of songs being displayed.
    total_displayed_songs = settings.LIMIT_UPCOMING_SONGS_DISPLAY
    upcoming_requested_tracks = SongRequest.objects.filter(time_played__isnull=True).exclude(requester=None).order_by('time_requested')    
    if upcoming_requested_tracks.count() < total_displayed_songs:
        random_song_display_limit = total_displayed_songs - upcoming_requested_tracks.count()
        upcoming_random_tracks = SongRequest.objects.filter(time_played__isnull=True, requester=None).order_by('time_requested')[:random_song_display_limit]
    else:
        upcoming_random_tracks = None
        
    pagevars = {
        "page_title": "Song Queue",
        "recently_played_tracks": recently_played_tracks,
        "currently_playing_track": currently_playing_track,
        "upcoming_requested_tracks": upcoming_requested_tracks,
        "upcoming_random_tracks": upcoming_random_tracks,
    }

    context_instance = RequestContext(request)
    return render_to_response('song_list.html', pagevars, context_instance)