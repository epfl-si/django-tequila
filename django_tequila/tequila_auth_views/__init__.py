from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.models import Site, RequestSite
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
    
    tequila_client = TequilaClient(EPFLConfig(additional_params = additional_params,
                                        redirect_to = next_path,
                                        allows = allows_needed,
                                        service = service_name,
                                        allow_guests = True))
    
    request.session.set_test_cookie()
    
    return HttpResponseRedirect(tequila_client.login_url())
login = never_cache(login)

def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)    
    
    return HttpResponseRedirect('/')

def not_allowed(request):
    return HttpResponse("Not allowed")