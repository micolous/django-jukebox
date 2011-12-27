"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.music_db.models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'artist', 'album', 'title', 'genre', 'request_count', 'rating', 'get_local_path',
                    'allow_random_play')
    list_editable = ('artist', 'album', 'title', 'genre', 'allow_random_play')
    date_hierarchy = 'time_added'
    search_fields = ['title', 'artist', 'album', 'genre']
admin.site.register(Song, SongAdmin)
