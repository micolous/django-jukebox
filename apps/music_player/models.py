"""
This module houses all of the DB models for the default player app. This
includes stuff like song request queues and histories.
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.music_player.managers import SongRequestManager

class SongRequest(models.Model):
    """
    This model is a single song request from a User. When it is played,
    the time_played field is set to a non-None value. This removes it from
    the queue.
    """
    song = models.ForeignKey('music_db.Song')
    requester = models.ForeignKey(User, blank=True, null=True)
    time_requested = models.DateTimeField(auto_now_add=True)
    # When non-None, this request has been played.
    time_played = models.DateTimeField(blank=True, null=True)
    
    objects = SongRequestManager()

    class Meta:
        ordering = ['-id']
    
    def __unicode__(self):
        return "%s requests %s - %s" % (self.requester, self.artist, 
                                        self.title)