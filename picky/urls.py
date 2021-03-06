from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('picky.pages.views',
    url(r'^$', 'index', name='index'),
    url(r'^all_pages/$', 'all_pages', name='all_pages'),
    url(r'^all_pages/urls/$', 'all_page_names', name='all_page_names'),
    url(r'^new_page/$', 'create_page', name='create_page'),
    url(r'^new_page/(?P<page_slug>[^/]+)$', 'create_page', name='create_page'),
                       
    url(r'^page/(?P<page_slug>[^/]+)/$', 'view_page', name='view_page'),
    url(r'^page/(?P<page_slug>[^/]+)/edit/$', 'edit_page', name='edit_page'),
    url(r'^page/(?P<page_slug>[^/]+)/changes/$', 'view_page_changes', name='view_page_changes'),

    url(r'^page/(?P<page_slug>[^/]+)/actions/$', 'view_page_actions', name='view_page_actions'),
    url(r'^page/(?P<page_slug>[^/]+)/actions/delete/$', 'delete_page', name='delete_page'),

    url(r'^page/(?P<page_slug>[^/]+)/comments/$', 'view_page_comments', name='view_page_comments'),
)

urlpatterns += patterns('',
    url(r'^page/(?P<page_slug>[^/]+)/comments/new/$', 'picky.comments.views.new_comment', name='new_comment'),
    url(r'^page/(?P<page_slug>[^/]+)/comments/new/(?P<parent_id>\d+)/$', 'picky.comments.views.new_comment', name='new_comment'),

    url(r'^search/$', 'picky.pages.views.search', name='search'),

    url(r'^users/$', 'picky.users.views.all_users', name='all_users'),
    url(r'^users/create$', 'picky.users.views.create_user', name='create_user'),
    url(r'^users/edit/(?P<user_id>\d+)$', 'picky.users.views.edit_user', name='edit_user'),
    url(r'^users/delete/(?P<user_id>\d+)$', 'picky.users.views.delete_user', name='delete_user'),
    url(r'^user/login/$', 'picky.users.views.login_picker', name="login_picker"),
    url(r'^user/login/native/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login"),
    url(r'^user/logout/$', 'picky.users.views.logout_user', name="logout"),
    url(r'^user/not_active/$', 'picky.users.views.user_not_active', name="user_not_active"),

    # todo: organise URLs into pages/, meta/, and ajax/
    url(r'^settings/$', 'picky.site_config.views.configure_site', name='configure_site'),
    url(r'^meta/$', 'picky.site_config.views.view_meta', name='meta'),
    url(r'^meta/recent_changes/$', 'picky.pages.views.recent_changes', name='recent_changes'),
    url(r'^meta/debug/$', 'picky.pages.views.debug', name='debug'),
    url(r'^meta/debug_styling/$', 'picky.pages.views.debug_styling', name='debug_styling'),
)

urlpatterns += patterns('',
    # todo: move to /user/social/login
    url(r'', include('social_auth.urls')),
)

handler404 = 'picky.site_config.views.not_found'
