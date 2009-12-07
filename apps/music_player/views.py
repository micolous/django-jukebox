"""
Views for Music Player interface.
"""
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.forms import ModelForm
from apps.music_db.models import Song
from apps.music_player.models import SongRequest
from includes.json import JSMessage

def music_player_main(request):
    """
    Main view for the music player.
    """
    pagevars = {
        "page_title": "Django JukeBox Beta",
    }

    context_instance = RequestContext(request)
    return render_to_response('index.html', pagevars, 
                              context_instance)

def display_song_queue(request):
    """
    Display the song queue. Previously played, currently playing, upcoming
    user requests, then upcoming random requests.
    """
    currently_playing_track = SongRequest.objects.filter(time_played__isnull=False).order_by('-time_played')[0]
    recently_played_tracks = SongRequest.objects.filter(time_played__isnull=False).exclude(id=currently_playing_track.id).order_by('-time_played')[:settings.NUMBER_OF_PREVIOUS_SONGS_DISPLAY]
    
    """
    Determine total number of songs being displayed. Display as many songs as
    have been requested by users, but if that number is less than the 
    LIMIT_UPCOMING_SONGS_DISPLAY setting, fill out with randomly generated requests
    until that number is reached.
    """
    total_displayed_songs = settings.LIMIT_UPCOMING_SONGS_DISPLAY
    upcoming_requested_tracks = SongRequest.objects.filter(time_played__isnull=True).exclude(requester=None).order_by('time_requested')    
    if upcoming_requested_tracks.count() < total_displayed_songs:
        random_song_display_limit = total_displayed_songs - upcoming_requested_tracks.count()
        upcoming_random_tracks = SongRequest.objects.filter(time_played__isnull=True, 
                                                            requester=None).order_by('time_requested')[:random_song_display_limit]
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
    return render_to_response('song_list.html', pagevars, 
                              context_instance)

class SongSearchForm(forms.Form):
    """
    Search form model. Only one field that will search across multiple columns.
    """
    keyword = forms.CharField()

def song_search(request):
    """
    Search form for songs. Find songs, request them... pretty basic.
    """
    pagevars = {
        "page_title": "Song Search",
        "form": SongSearchForm(),
    }
    
    context_instance = RequestContext(request)
    return render_to_response('song_search.html', pagevars, 
                              context_instance)
        
def song_search_results(request, qset=Song.objects.all()):
    """
    Query Song model based on search input.
    """
    form = SongSearchForm(request.POST)
    
    if request.POST and form.is_valid():
        s_search = form.cleaned_data.get("keyword", None)
        if s_search:
            qset = qset.filter(artist__icontains=s_search)
    else:
        qset.order_by('?')[:10]
        
    pagevars = {
            "page_title": "Song Search Results",
            "qset": qset,
            }
    
    context_instance = RequestContext(request)
    return render_to_response('song_results.html', pagevars, 
                              context_instance)
            
def request_song(request, song_id):
    """
    Request the song.
    """
    song = Song.objects.get(id=song_id)
    request = SongRequest(song=song,
                          requester=request.user)
    request.save()
    return HttpResponse(JSMessage("Song Requested."))