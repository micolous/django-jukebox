"""
This module houses all of the DB models for the default player app. This
includes stuff like song request queues and histories.
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import signals
from apps.music_player.managers import SongRequestManager

class SongRequest(models.Model):
    """
    This model is a single song request from a User. When it is played,
    the time_played field is set to a non-None value. This removes it from
    the queue.
    """
    song = models.ForeignKey('music_db.Song')
    requester = models.ForeignKey(User, blank=True, null=True)
    # Does this song meet the 'upcoming' classification?
    is_upcoming_song = models.BooleanField(default=False)
    # Does this song meet the 'good' classification?
    is_good_song = models.BooleanField(default=False)
    time_requested = models.DateTimeField(auto_now_add=True)
    # When non-None, this request has been played.
    time_played = models.DateTimeField(blank=True, null=True)
    
    objects = SongRequestManager()

    class Meta:
        ordering = ['id']
    
    def __unicode__(self):
        return "%s requests %s - %s" % (self.requester, self.song.artist, 
                                        self.song.title)
        
def songrequest_pre_save(sender, instance, *args, **kwargs):
    """
    Do some denormalization to make our playlist generator a little
    more simple.
    """
    if instance.song.rating == None or \
        instance.song.num_ratings < settings.RANDOM_REQ_UPCOMING_MAX_RATINGS:
        instance.is_upcoming_song = True
    else:
        instance.is_upcoming_song = False
        if instance.song.rating > settings.RANDOM_REQ_GOOD_RATING and \
            instance.song.num_ratings > settings.RANDOM_REQ_UPCOMING_MAX_RATINGS:
            instance.is_good_song = True
        else:
            instance.is_good_song = False
signals.pre_save.connect(songrequest_pre_save, sender=SongRequest)