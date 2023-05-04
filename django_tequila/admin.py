"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

try:
    # For python 2
    import urlparse
except ImportError:
    # For python 3
    from urllib import parse as urlparse

from functools import update_wrapper

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseForbidden, HttpResponseRedirect, QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


class TequilaAdminSite(AdminSite):
    def admin_view(self, view, cacheable=False):
        """
        Verify that the user is logged, and he has the right to access it
        """

        def inner(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return self.login(request)
            if not self.has_permission(request):
                return self.not_allowed_redirect(request)
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    @method_decorator(never_cache)
    def login(self, request, extra_context=None):
        """
        Don't display the login form, use the Tequila login process instead
        """
        # user is not logged, so redirect to the real login
        try:
            login_url = settings.LOGIN_URL
        except AttributeError:
            raise ImproperlyConfigured(
                "You have to set a LOGIN_URL in your settings.py")

        next_url = request.get_full_path()
        login_url_parts = list(urlparse.urlparse(login_url))
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[REDIRECT_FIELD_NAME] = next_url
        login_url_parts[4] = querystring.urlencode(safe='/')

        return HttpResponseRedirect(urlparse.urlunparse(login_url_parts))

    def not_allowed_redirect(self, request):
        try:
            not_allowed_login_url = settings.LOGIN_REDIRECT_IF_NOT_ALLOWED
            return HttpResponseRedirect(not_allowed_login_url)
        except AttributeError:
            return HttpResponseForbidden("Access forbidden")
