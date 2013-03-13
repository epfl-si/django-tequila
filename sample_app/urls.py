from django.conf.urls.defaults import *
from django_tequila.urls import urlpatterns as django_tequila_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'views.index', name="index"),
    url(r'^protected/$', 'views.protected_view', name='protected'),
    url(r'^unprotected/$', 'views.unprotected_view', name='unprotected'),
)

urlpatterns += django_tequila_urlpatterns
