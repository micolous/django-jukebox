import os
import mutagen
from mutagen.id3 import ID3
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
    
    def populate_from_id3_tags(self, file_path=None):
        """    
        Read ID3 tags of the mp3 file.
        
        file: (string) Path to a file to load from instead of the default
                       one for this object.
        """
        if not file_path:
            # Assume the object's file field unless otherwise specified.
            file_path = self.file
        try:
            tag = ID3(file_path)
            print tag
            # Map ID3 tags to columns in the Song table.
            # ID3 Reference: http://www.id3.org/id3v2.4.0-frames
            try:
                self.title = str(tag['TIT2'])
            except KeyError:
                pass
            
            try:
                self.artist = str(tag['TPE1'])
            except KeyError:
                pass
            
            try:
                self.album = str(tag['TALB'])
            except KeyError:
                pass
            
            try:
                self.genre = str(tag['TCON'])
            except KeyError:
                pass
            
            # Track numbers are stored in ID3 tags as '1/10' (track/total tracks)
            # Split and just store the track number.
            try:
                self.track_number = str(tag['TRCK']).split('/')[0]
            except KeyError:
                pass
            
        except mutagen.id3.ID3NoHeaderError:
            print 'Warning: NoID3Header'
        
def song_pre_save(sender, instance, *args, **kwargs):
    """
    Things to happen in the point of saving an song before the actual save()
    call happens.
    """
    # If the Item has a Null or False value for its 'id' field, it's a new
    # item. Give it a new num_in_job.
    if not instance.id:
        # New Song, scan ID3 tags for file.
        temp_upload_file = instance.file.file.temporary_file_path()
        instance.populate_from_id3_tags(file_path=temp_upload_file)
signals.pre_save.connect(song_pre_save, sender=Song)

def song_pre_delete(sender, instance, *args, **kwargs):
    """
    Clean up misc. stuff before a Song is deleted.
    """
    instance.file.delete()
signals.pre_delete.connect(song_pre_delete, sender=Song)