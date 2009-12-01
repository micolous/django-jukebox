from django.db import models
from django.conf import settings
from django.db.models import signals

class Song(models.Model):
    """
    This model represents a single song in the library.
    """
    title = models.CharField(max_length=255, default="Unknown")
    artist = models.CharField(max_length=255, default="Unknown")
    album = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=255, blank=True)
    # Song length (seconds)
    length = models.IntegerField(blank=True, null=True)
    track_number = models.IntegerField(blank=True, null=True)
    disc_number = models.IntegerField(blank=True, null=True)
    # If this is True, allow this song to be selected by the random
    # playback mechanism (in the absence of any queue entries).
    allow_random_play = models.BooleanField(default=True)
    # Number of times the song has been requested.
    request_count = models.IntegerField(default=0)
    # Average of all ratings for this song.
    rating = models.FloatField(blank=True, null=True)
    file = models.FileField(upload_to=settings.MUSIC_DIR_NAME, max_length=255)
    # When the song was added to the library.
    time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['artist', 'disc_number', 'track_number', 'title']
    
    def __unicode__(self):
        return "%s - %s" % (self.artist, self.title)
    
def song_pre_delete(sender, instance, *args, **kwargs):
    """
    Clean up misc. stuff before a Song is deleted.
    """
    instance.file.delete()
signals.pre_delete.connect(song_pre_delete, sender=Song)