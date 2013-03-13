from django.conf.urls.defaults import *

from django_tequila.urls import urlpatterns as django_tequila_urlpatterns

from django.contrib import admin
from django_tequila.admin import TequilaAdminSite

admin.autodiscover()
admin.site.__class__ = TequilaAdminSite

urlpatterns = patterns('',
    url(r'^$', 'sample_app.views.index', name="index"),
    url(r'^protected/$', 'sample_app.views.protected_view', name='protected'),
    url(r'^unprotected/$', 'sample_app.views.unprotected_view', name='unprotected'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += django_tequila_urlpatterns