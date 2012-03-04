from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^users/$', 'users.views.all_users', name='all_users'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)
