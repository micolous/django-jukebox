"""
Module for requesting random songs in the absence of any requests
originating from authenticated users.
"""
from django.conf import settings
from apps.music_db.models import Song
from apps.music_player import SongRequest

def request_random_good_songs(num_songs):
    pass

def request_random_upcoming_songs(num_songs):
    pass

def fill_random_request_queue():
    """
    Determines how many anonymous requests are queued up, and tops them off
    based on the values in settings.py.
    """
    anon_queue = SongRequest.objects.get_pending_anonymous_requests()
    
    good_songs = anon_queue.filter(song__rating__gte=settings.RANDOM_REQ_GOOD_RATING)  
    good_song_diff = settings.RANDOM_REQ_GOOD_RATED_SONGS - good_songs.count()
    if good_song_diff > 0:
        request_random_good_songs(good_song_diff)
    
    upcoming_songs = anon_queue.exclude(song__rating__gte=settings.RANDOM_REQ_GOOD_RATING)    
    upcoming_song_diff = settings.RANDOM_REQ_UPCOMING - upcoming_songs.count()
    if upcoming_song_diff > 0:
        request_random_upcoming_songs(upcoming_song_diff) 