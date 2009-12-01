"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.music_db.models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('artist', 'album', 'title', 'disc_number', 'track_number',
                    'genre', 'request_count', 'rating', 'file',
                    'allow_random_play')
    date_hierarchy = 'time_added'
    search_fields = ['title', 'artist', 'genre']
admin.site.register(Song, SongAdmin)