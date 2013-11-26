try:
    from django.conf.urls import patterns, url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'django_tequila.tequila_auth_views.login', name='login_view'),
    url(r'^logout/$', 'django_tequila.tequila_auth_views.logout', name='logout'),
    url(r'^not_allowed/$', 'django_tequila.tequila_auth_views.not_allowed', name='not_allowed'),
)