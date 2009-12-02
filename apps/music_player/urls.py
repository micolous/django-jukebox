from django.conf.urls.defaults import *

urlpatterns = patterns('django_jukebox.apps.music_player.views',
    url(r'^$', 'music_player_main', name='music_player_main'),
)
