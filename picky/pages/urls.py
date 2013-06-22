from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^pages/$', 'pages.views.all_pages', name='all_pages'),
    url(r'^pages/new/$', 'pages.views.create_page', name='create_page'),
    url(r'^pages/history/(?P<page_id>\d+)$', 'pages.views.view_page_history', name='view_page_history'),
    url(r'^pages/edit/(?P<page_id>\d+)$', 'pages.views.edit_page', name='edit_page'),
                       
    url(r'^pages/actions/(?P<page_id>\d+)$', 'pages.views.view_page_actions', name='page_actions'),
    url(r'^pages/delete/(?P<page_id>\d+)$', 'pages.views.delete_page', name='delete_page'),

    url(r'^pages/new_comment/(?P<page_id>\d+)$', 'comments.views.new_comment', name='new_comment'),
                       

    url(r'^page/(?P<page_slug>.*)$', 'pages.views.view_page', name='view_page'),
)
