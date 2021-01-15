"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.conf.urls import url
from django.contrib import admin

from django_tequila.admin import TequilaAdminSite
from django_tequila.urls import urlpatterns as django_tequila_urlpatterns
from django_tequila_app.views import index, protected_view, unprotected_view

admin.autodiscover()
admin.site.__class__ = TequilaAdminSite

urlpatterns = [
    url(r'^$', index,
        name="index"),
    url(r'^protected/$', protected_view,
        name='protected'),
    url(r'^unprotected/$', unprotected_view,
        name='unprotected'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += django_tequila_urlpatterns
