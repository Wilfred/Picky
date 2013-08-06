from django.conf.urls.defaults import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'pages.views.index', name='index'),
    url(r'^all_pages/$', 'pages.views.all_pages', name='all_pages'),
    url(r'^new_page/$', 'pages.views.create_page', name='create_page'),
    url(r'^new_page/(?P<page_slug>[^/]+)$', 'pages.views.create_page', name='create_page'),
                       
    url(r'^page/(?P<page_slug>[^/]+)/$', 'pages.views.view_page', name='view_page'),
    url(r'^page/(?P<page_slug>[^/]+)/edit/$', 'pages.views.edit_page', name='edit_page'),
    url(r'^page/(?P<page_slug>[^/]+)/history/$', 'pages.views.view_page_history', name='view_page_history'),

    url(r'^page/(?P<page_slug>[^/]+)/actions/$', 'pages.views.view_page_actions', name='view_page_actions'),
    url(r'^page/(?P<page_slug>[^/]+)/actions/delete/$', 'pages.views.delete_page', name='delete_page'),

    url(r'^page/(?P<page_slug>[^/]+)/comments/$', 'pages.views.view_page_comments', name='view_page_comments'),
    url(r'^page/(?P<page_slug>[^/]+)/comments/new/$', 'comments.views.new_comment', name='new_comment'),

    url(r'^users/$', 'users.views.all_users', name='all_users'),
    url(r'^users/create$', 'users.views.create_user', name='create_user'),
    url(r'^users/edit/(?P<user_id>\d+)$', 'users.views.edit_user', name='edit_user'),
    url(r'^users/delete/(?P<user_id>\d+)$', 'users.views.delete_user', name='delete_user'),
    url(r'^user/login/$', 'users.views.login_picker', name="login_picker"),
    url(r'^user/login/native/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login"),
    url(r'^user/logout/$', 'users.views.logout_user', name="logout"),

    url(r'^settings/$', 'site_config.views.configure_site', name='configure_site'),
    url(r'^meta/$', 'site_config.views.view_meta', name='meta'),

    # todo: move to /user/social/login
    url(r'', include('social_auth.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'site_config.views.not_found'
