"""
Module for requesting random songs in the absence of any requests
originating from authenticated users.
"""
import random
from itertools import chain
from django.conf import settings
from django.db.models import Q
from apps.music_db.models import Song
from apps.music_player.models import SongRequest

def enqueue_song(song):
    """
    Given a Song object, create a SongRequest.
    
    song: (Song) The Song object to enqueue.
    """
    new_request = SongRequest(song=song)
    new_request.save()

def find_random_good_songs(num_songs):
    """
    Finds a pre-determined number of 'good' songs.
    
    num_songs: (int) Number of songs to find (max). You won't necessarily
                     get this many if there aren't enough matches.
    """
    return Song.objects.get_good_songs().order_by('?')[:settings.RANDOM_REQ_GOOD_RATED_SONGS]

def find_random_upcoming_songs(num_songs):
    """
    Find a pre-determined number of 'upcoming' songs. This means that the songs
    either have no ratings, or only a few, as per capped by
    settings.RANDOM_REQ_UPCOMING_MAX_RATINGS.
    
    num_songs: (int) Number of songs to find (max). You won't necessarily
                     get this many if there aren't enough matches.
    """
    return Song.objects.get_upcoming_songs().order_by('?')[:settings.RANDOM_REQ_UPCOMING]

def fill_random_request_queue():
    """
    Determines how many anonymous requests are queued up, and tops them off
    based on the values in settings.py.
    """
    anon_queue = SongRequest.objects.get_pending_anonymous_requests()
       
    queued_good_songs = anon_queue.filter(is_good_song=True)
    good_song_diff = settings.RANDOM_REQ_GOOD_RATED_SONGS - queued_good_songs.count()
    if good_song_diff > 0:
        #print "Need %d good songs" % good_song_diff
        good_songs_to_add = find_random_good_songs(good_song_diff)
    else:
        good_songs_to_add = []
    
    queued_upcoming_songs = anon_queue.filter(is_upcoming_song=True)    
    upcoming_song_diff = settings.RANDOM_REQ_UPCOMING - queued_upcoming_songs.count()
    if upcoming_song_diff > 0:
        #print "Need %d upcoming songs" % upcoming_song_diff
        upcoming_songs_to_add = find_random_upcoming_songs(upcoming_song_diff)
    else:
        upcoming_songs_to_add = []
        
    songs_to_add = list(chain(good_songs_to_add, upcoming_songs_to_add))
    random.shuffle(songs_to_add)
    
    #print "SONGS (%d): %s" % (len(songs_to_add), songs_to_add)
    for song in songs_to_add:
        enqueue_song(song)