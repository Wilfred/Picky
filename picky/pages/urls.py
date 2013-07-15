from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'pages.views.index', name='index'),
    url(r'^all_pages/$', 'pages.views.all_pages', name='all_pages'),
    url(r'^new_page/$', 'pages.views.create_page', name='create_page'),
    url(r'^new_page/(?P<page_slug>[^/]+)$', 'pages.views.create_page', name='create_page'),
                       
    url(r'^page/(?P<page_slug>[^/]+)$', 'pages.views.view_page', name='view_page'),
    url(r'^page/(?P<page_slug>[^/]+)/edit/$', 'pages.views.edit_page', name='edit_page'),
    url(r'^page/(?P<page_slug>[^/]+)/history/$', 'pages.views.view_page_history', name='view_page_history'),

    url(r'^page/(?P<page_slug>[^/]+)/actions/$', 'pages.views.view_page_actions', name='view_page_actions'),
    url(r'^page/(?P<page_slug>[^/]+)/actions/delete/$', 'pages.views.delete_page', name='delete_page'),

    url(r'^page/(?P<page_slug>[^/]+)/comments/$', 'pages.views.view_page_comments', name='view_page_comments'),
    url(r'^page/(?P<page_slug>[^/]+)/comments/new/$', 'comments.views.new_comment', name='new_comment'),
)
