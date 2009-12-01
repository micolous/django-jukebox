"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.music_db.models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'disc_number', 'track_number',
                    'length', 'request_count', 'rating', 'genre', 'file',
                    'allow_random_play')
    date_hierarchy = 'time_added'
    search_fields = ['title', 'artist', 'genre']
admin.site.register(Song, SongAdmin)