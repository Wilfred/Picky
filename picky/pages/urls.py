from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^pages/$', 'pages.views.all_pages', name='all_pages'),
    url(r'^pages/new/$', 'pages.views.create_page', name='create_page'),
)
