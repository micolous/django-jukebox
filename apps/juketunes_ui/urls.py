from django.conf.urls.defaults import *

urlpatterns = patterns('apps.juketunes_ui.views.main',
    url(r'^$', 'view_main', 
        name='juketunes_ui-main'),  
)
