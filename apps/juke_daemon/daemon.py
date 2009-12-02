import time
from apps.music_player.models import SongRequest

def start_daemon_loop():
    while True:
        auth_requests = SongRequest.objects.get_pending_user_requests()
        if auth_requests:
            print "PLAYING - %s" % auth_requests[0]
        else:
            anon_requests = SongRequest.objects.get_pending_anonymous_requests()
            if anon_requests:
                print "PLAYING ANON - %s" % anon_requests[0]
            else:
                # No songs in queue, sleep for a while and try again.
                # This should not happen unless the cron process to fill the
                # queue is barfed up.
                print "No songs in queue, sleeping."
                time.sleep(10)