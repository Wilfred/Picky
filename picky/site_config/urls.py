from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^settings/$', 'site_config.views.configure_site', name='configure_site'),
)