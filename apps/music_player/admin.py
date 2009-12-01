"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.music_player.models import SongRequest

class SongRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'song', 'time_requested', 'time_played')
    date_hierarchy = 'time_requested'
    search_fields = ['song__title', 'song__artist', 'song__genre']
admin.site.register(SongRequest, SongRequestAdmin)