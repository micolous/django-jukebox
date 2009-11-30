from django.db import models
from django.conf import settings

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True)
    # Song length (seconds)
    length = models.IntegerField(blank=True, null=True)
    track_number = models.IntegerField(blank=True, null=True)
    disc_number = models.IntegerField(blank=True, null=True)
    # Number of times the song has been requested.
    request_count = models.IntegerField(default=0)
    # Average of all ratings for this song.
    rating = models.FloatField(blank=True, null=True)
    file = models.FileField(upload_to=settings.MUSIC_DIR_NAME, max_length=255)

    class Meta:
        ordering = ['artist', 'disc_number', 'track_number', 'title']
    
    def __unicode__(self):
        return "%s - %s" % (self.artist, self.title)