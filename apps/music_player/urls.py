from django.conf.urls.defaults import *

urlpatterns = patterns('django_jukebox.apps.music_player.views',
    url(r'^$', 'music_player_main', name='music_player_main'),
    url(r'^song_queue/$', 'display_song_queue', name='music_player-display_song_queue'),
)
