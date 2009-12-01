"""
Module for requesting random songs in the absence of any requests
originating from authenticated users.
"""
from django.conf import settings
from django.db.models import Q
from apps.music_db.models import Song
from apps.music_player.models import SongRequest

def find_random_good_songs(num_songs):
    """
    Finds a pre-determined number of 'good' songs.
    
    num_songs: (int) Number of songs to find (max). You won't necessarily
                     get this many if there aren't enough matches.
    """
    return Song.objects.filter(rating__gte=settings.RANDOM_REQ_GOOD_RATING).order_by('?')[:settings.RANDOM_REQ_GOOD_RATED_SONGS]

def find_random_upcoming_songs(num_songs):
    """
    Find a pre-determined number of 'upcoming' songs. This means that the songs
    either have no ratings, or only a few, as per capped by
    settings.RANDOM_REQ_UPCOMING_MAX_RATINGS.
    
    num_songs: (int) Number of songs to find (max). You won't necessarily
                     get this many if there aren't enough matches.
    """
    return Song.objects.filter(Q(rating__isnull=True) | 
            Q(num_ratings__lte=settings.RANDOM_REQ_UPCOMING_MAX_RATINGS)
            ).order_by('?')[:settings.RANDOM_REQ_UPCOMING]

def fill_random_request_queue():
    """
    Determines how many anonymous requests are queued up, and tops them off
    based on the values in settings.py.
    """
    anon_queue = SongRequest.objects.get_pending_anonymous_requests()
    
    queued_good_songs = anon_queue.filter(song__rating__gte=settings.RANDOM_REQ_GOOD_RATING)  
    good_song_diff = settings.RANDOM_REQ_GOOD_RATED_SONGS - queued_good_songs.count()
    if good_song_diff > 0:
        find_random_good_songs(good_song_diff)
    
    queued_upcoming_songs = anon_queue.exclude(song__rating__gte=settings.RANDOM_REQ_GOOD_RATING)    
    upcoming_song_diff = settings.RANDOM_REQ_UPCOMING - queued_upcoming_songs.count()
    if upcoming_song_diff > 0:
        find_random_upcoming_songs(upcoming_song_diff) 