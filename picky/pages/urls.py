from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^pages/$', 'pages.views.all_pages', name='all_pages'),
    url(r'^pages/new/$', 'pages.views.create_page', name='create_page'),
    url(r'^pages/edit/(?P<page_id>\d+)$', 'pages.views.edit_page', name='edit_page'),
    url(r'^pages/delete/(?P<page_id>\d+)$', 'pages.views.delete_page', name='delete_page'),

    url(r'^page/(?P<page_slug>.*)$', 'pages.views.view_page', name='view_page'),
)
