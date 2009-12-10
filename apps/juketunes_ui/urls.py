from django.conf.urls.defaults import *

urlpatterns = patterns('apps.juketunes_ui.views.main',
    url(r'^$', 'view_main', name='juketunes_ui-main'),
)

urlpatterns += patterns('apps.juketunes_ui.views.ajax',
    url(r'^ajax/get_artist_list/$', 'ajax_get_artist_list', 
        name='juketunes_ui-ajax_get_artist_list'),
)