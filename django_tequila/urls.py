'''
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
'''

from django.conf.urls import url
from django_tequila.tequila_auth_views import login, logout, not_allowed

urlpatterns = [
    url(r'^login/?$', login, name='login_view'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^not_allowed/$', not_allowed, name='not_allowed'),
]
