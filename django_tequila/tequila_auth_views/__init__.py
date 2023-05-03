"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2020
"""

from django.contrib.auth import get_user_model
from django.contrib.auth import REDIRECT_FIELD_NAME

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from django_tequila.tequila_client import TequilaClient
from django_tequila.tequila_client import EPFLConfig



User = get_user_model()


def get_redirect_url(request):
    """Return the user-originating redirect URL if it's safe."""
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME)

    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=request.get_host(),
        require_https=request.is_secure(),
    )
    return redirect_to if url_is_safe else ''


def login(request):
    if request.GET.get(REDIRECT_FIELD_NAME):
        next_path = request.GET[REDIRECT_FIELD_NAME]
    else:
        next_path = settings.LOGIN_REDIRECT_URL

    # fullfill domain for tequila, and for security reasons
    if next_path and next_path[0] == '/':
        next_path = next_path[1:]

    next_path = request.get_host() + '/' + next_path

    if request.is_secure():
        next_path = 'https://' + next_path
    else:
        next_path = 'http://' + next_path

    if request.user.is_authenticated:
        return HttpResponseRedirect(next_path)

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
        allow_guests = settings.TEQUILA_ALLOW_GUESTS
    except AttributeError:
        allow_guests = False


    tequila_client = TequilaClient(
        EPFLConfig(
            server_url=server_url,
            additional_params=additional_params,
            redirect_to=next_path,
            allows=allows_needed,
            service=service_name,
            allow_guests=allow_guests,
            strong_authentication=strong_authentication,
        ))

    request.session.set_test_cookie()

    return HttpResponseRedirect(tequila_client.login_url())


login = never_cache(login)


def logout(request):
    next_path = get_redirect_url(request)

    if not next_path:
        next_path = settings.LOGOUT_URL

    from django.contrib.auth import logout as auth_logout
    auth_logout(request)

    return HttpResponseRedirect(next_path)


def not_allowed(request):
    try:
        not_allowed_text = settings.LOGIN_REDIRECT_TEXT_IF_NOT_ALLOWED
    except AttributeError:
        not_allowed_text = "Not allowed"
    return HttpResponse(not_allowed_text)
