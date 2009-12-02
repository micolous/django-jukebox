"""
This module contains the jukebox daemon server. The idea is to check for an 
SongRequest objects that have no time_played value. The daemon will play each 
of these in order via a simple loop.
"""
import time
import datetime
from subprocess import call
from django.conf import settings
from apps.music_player.models import SongRequest

def play_song(request):
    """
    Plays the song associated with a SongRequest object.
    
    request: (SongRequest) The request to play.
    """
    request.time_played = datetime.datetime.now()
    request.save()
    print "Playing: %s" % request
    cmd_list = settings.CLI_PLAYER_COMMAND_STR + [request.song.file.path]
    call(cmd_list)

def daemon_loop():
    """
    This infinite loop goes through and checks the SongRequest queue,
    playing the requests in order. If none are found, the process sleeps and
    checks the queue at a later time.
    """
    while True:
        # First check for authenticate User requests, these get top priority.
        auth_requests = SongRequest.objects.get_pending_user_requests()
        if auth_requests:
            # Play the first authenticated User's request.
            play_song(auth_requests[0])
        else:
            # No User requests found, check one of the anonymous requests.
            # These are usually from the random_requester.py module.
            anon_requests = SongRequest.objects.get_pending_anonymous_requests()
            if anon_requests:
                # Play the first anonymously requested song.
                play_song(anon_requests[0])
            else:
                # No songs in queue, sleep for a while and try again.
                # This should not happen unless the cron process to fill the
                # queue is barfed up.
                print "No songs in queue, sleeping."
                time.sleep(settings.TIME_TO_SLEEP_WHEN_QUEUE_EMPTY)