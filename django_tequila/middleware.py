from django.conf import settings
from django.contrib import auth
from django.contrib.auth.middleware import PersistentRemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured

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
    
    for k, v in p.items():
        if isinstance(v, (list,tuple)):
            p[k] = v[0]
    
    return '?%s' % urlencode(p)

class TequilaMiddleware(PersistentRemoteUserMiddleware):
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
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the TequilaMiddleware class.")
        # If the user is already authenticated, her is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            return

        try:
            # Django diff : key is provided by GET, not META
            tequila_key = request.GET[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return
        
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(tequila_key = tequila_key)

        # deny page if not allowed
        if not user:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_IF_NOT_ALLOWED)
        else:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

            try:
                clean_url = settings.TEQUILA_CLEAN_URL
                
                if clean_url:
                    #get the url, remove key and redirect to it
                    cleaned_url = request.path
                    
                    #QueryDict to dict
                    params = dict(request.GET.iterlists())
                    
                    cleaned_url += get_query_string(params, remove=self.header)
                    return HttpResponseRedirect(cleaned_url)

            except AttributeError:
                pass    
