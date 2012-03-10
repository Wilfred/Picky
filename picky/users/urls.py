from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^users/$', 'users.views.all_users', name='all_users'),
    url(r'^users/create$', 'users.views.create_user', name='create_user'),
    url(r'^user/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login"),
    url(r'^user/logout/$', 'users.views.logout_user', name="logout"),
)
