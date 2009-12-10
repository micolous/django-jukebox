from django.conf.urls.defaults import *

# Generic views that don't require actual internal view code of their own.
urlpatterns = patterns('django.contrib.auth.views',
    url(r'^logout/$', 'logout_then_login', name='logout'),
    url(r'^login/$', 'login', {'template_name': 'login.html'}, name='login'),
)