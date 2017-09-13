"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django_tequila.tequila_client import TequilaClient
from django_tequila.tequila_client import EPFLConfig
from django.conf import settings

def login(request):
    if request.GET.get(REDIRECT_FIELD_NAME):
        next_path = request.GET[REDIRECT_FIELD_NAME]
    else:
        next_path = settings.LOGIN_REDIRECT_URL
    
    if request.user.is_authenticated():
        return HttpResponseRedirect(next_path)
    
    # fullfill domain for tequila
    next_path = request.get_host() + next_path

    if request.is_secure():
        next_path = 'https://' + next_path
    else:
        next_path = 'http://' + next_path
    
    try:
        server_url = settings.TEQUILA_SERVER_URL
    except AttributeError:
        server_url = ""     
    
    try:
        additional_params = settings.TEQUILA_CONFIG_ADDITIONAL
    except AttributeError:
        additional_params = None

    try:
        allows_needed = settings.TEQUILA_CONFIG_ALLOW
    except AttributeError:
        allows_needed = None

    try:
        service_name = settings.TEQUILA_SERVICE_NAME
    except AttributeError:
        service_name = 'Unknown application'
        
    try:
        strong_authentication = settings.TEQUILA_STRONG_AUTHENTICATION
    except AttributeError:
        strong_authentication = False

    try:
        force_redirect_https = settings.TEQUILA_FORCE_REDIRECT_HTTPS
    except AttributeError:
        force_redirect_https = False

    tequila_client = TequilaClient(EPFLConfig(server_url = server_url,
                                        additional_params = additional_params,
                                        redirect_to = next_path,
                                        allows = allows_needed,
                                        service = service_name,
                                        allow_guests = True,
                                        strong_authentication = strong_authentication,
                                        force_redirect_https = force_redirect_https,
                                        ))
    
    request.session.set_test_cookie()
    
    return HttpResponseRedirect(tequila_client.login_url())
login = never_cache(login)

def logout(request):
    if request.GET.get(REDIRECT_FIELD_NAME):
        next_path = request.GET[REDIRECT_FIELD_NAME]
    else:
        next_path = settings.LOGOUT_URL

    from django.contrib.auth import logout as auth_logout
    auth_logout(request)    
    
    return HttpResponseRedirect(next_path)

def not_allowed(request):
    return HttpResponse("Not allowed")