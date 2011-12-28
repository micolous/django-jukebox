from django.conf.urls.defaults import *

# Generic views that don't require actual internal view code of their own.
urlpatterns = patterns('django.contrib.auth.views',
	url(
		r'^logout/$',
		'logout_then_login',
		name='logout'
	),
	
	url(
		r'^login/$',
		'login',
		dict(
			template_name='login.html'
		),
		name='login'
	),
	
	url(
		r'^change_password/$',
		'password_change',
		dict(
			template_name='password_change_form.html'
		),
		name='change_password'
	),
	
	url(
		r'^change_password/done/$',
		'password_change_done',
		dict(
			template_name='password_change_done.html'
		),
		name='password_change_done'
	),
)