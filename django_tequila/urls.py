"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

# from django.conf.urls import url
from django.urls import re_path

from django_tequila.tequila_auth_views import login, logout, not_allowed

urlpatterns = [
    re_path(r'^login/?$', login, name='login_view'),
    re_path(r'^logout/$', logout, name='logout'),
    re_path(r'^not_allowed/$', not_allowed, name='not_allowed'),
]
