from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^users/$', 'users.views.all_users', name='all_users'),
)
