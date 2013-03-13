from django.contrib.auth.middleware import AuthenticationMiddleware, RemoteUserMiddleware
from django.contrib import auth
from django.contrib.auth import views
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.http import HttpResponseRedirect

from django.utils.http import urlencode

def get_query_string(params, new_params=None, remove=None):
    """ Allow to rewrite params from url """
    if new_params is None: new_params = {}
    if remove is None: remove = []
    p = params.copy()
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    return '?%s' % urlencode(p)

class TequilaMiddleware(RemoteUserMiddleware):
    """
    Middleware for utilizing tequila web-server-provided authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate with the key passed in the ``key`` request.GET.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    """

    # Name of request key to grab the key from
    header = "key"
    
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            return 
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the TequilaMiddleware class.")
        # If the user is already authenticated, her is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            return
        try:
            tequila_key = request.GET[self.header]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(tequila_key = tequila_key)
        
        if not self.is_user_allowed(user):
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_IF_NOT_ALLOWED)
        
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

            try:
                clean_url = settings.TEQUILA_CLEAN_URL
                
                if clean_url:
                    #get the url, remove key and redirect to it
                    cleaned_url = request.path
                    cleaned_url += get_query_string(request.GET, remove=self.header)
                    return HttpResponseRedirect(cleaned_url)

            except AttributeError:
                pass    

    def is_user_allowed(self, user):
        """
        Additional validation
        """
        return user.is_active

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError: # Backend has no clean_username method.
            pass
        return username