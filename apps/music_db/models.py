import os
import mutagen
from mutagen.id3 import ID3
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import signals
from apps.music_db.managers import SongManager

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
    # Cache number of ratings for easier querying in playlist generation.
    num_ratings = models.IntegerField(default=0)
    file = models.FileField(upload_to=settings.MUSIC_DIR_NAME, max_length=255)
    # Who added (uploaded) the Song.
    added_by = models.ForeignKey(User, blank=True, null=True)
    # When the song was added to the library.
    time_added = models.DateTimeField(auto_now_add=True)
    # The time the song was last played, requested or automatically.
    time_last_played = models.DateTimeField(blank=True, null=True)
    # Time the song was specifically requested to play.
    time_last_requested = models.DateTimeField(blank=True, null=True)
    
    objects = SongManager()

    class Meta:
        ordering = ['artist', 'album', 'disc_number', 'track_number', 'title']
    
    def __unicode__(self):
        return "%s - %s" % (self.artist, self.title)
    
    def populate_from_id3_tags(self, file_path, file_name):
        """    
        Read ID3 tags of the mp3 file.
        
        file_path: (str) Path to a file to load ID3 tags from. This is
                         generally supplied by song_pre_save().
        file_name: (str) When uploading files from a browser, a temporary
                         file is used through much of the process. This is
                         passed so that the file name may be used when invalid
                         or no tags are found, instead of the scrambled file
                         name that the temporary upload file uses.
        """
        try:
            tag = ID3(file_path)
            #print tag
            # Map ID3 tags to columns in the Song table.
            # ID3 Reference: http://www.id3.org/id3v2.4.0-frames
            try:
                self.title = str(tag['TIT2'])
            except KeyError:
                # No tag for title found, use file name.
                self.title = file_name
            
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
            # Invalid ID3 headers. Just use the file name as the title.
            self.title = file_name
        
def song_pre_save(sender, instance, *args, **kwargs):
    """
    Things to happen in the point of saving an song before the actual save()
    call happens.
    """
    # If the Item has a Null or False value for its 'id' field, it's a new
    # item. Give it a new num_in_job.
    if not instance.id:
        # The file name is used when there are no ID3 tags indicating title.
        file_name = os.path.basename(instance.file.file.name)
        if hasattr(instance.file.file, 'temporary_file_path'):
            # This is probably being uploaded from a form. Use TempUploadFile
            # to figure out where the file is -currently- (before being saved).
            file_path = instance.file.file.temporary_file_path()
        else:
            # This song is being added via a script and is already probably
            # in the music directory.
            file_path = instance.file.path
        # New Song, scan ID3 tags for file.
        instance.populate_from_id3_tags(file_path, file_name)
signals.pre_save.connect(song_pre_save, sender=Song)

def song_pre_delete(sender, instance, *args, **kwargs):
    """
    Clean up misc. stuff before a Song is deleted.
    """
    instance.file.delete()
signals.pre_delete.connect(song_pre_delete, sender=Song)

class SongRating(models.Model):
    """
    Represents a rating for a song, as provided by an authenticated User.
    """
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    rating = models.FloatField()