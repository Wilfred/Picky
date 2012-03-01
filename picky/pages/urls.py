from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^pages/$', 'pages.views.all_pages', name='all_pages'),
)
