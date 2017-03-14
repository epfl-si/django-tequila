'''
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
'''

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

def index(request):
    c = Context({'user' : request.user})
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c))

@login_required
def protected_view(request):
    profile = ""

    if request.user.is_authenticated():
        profile = request.user.profile

    return HttpResponse("Successfully seeing a protected view.")
    
def unprotected_view(request):
    login_url = mark_safe('<a href="%s?next=%s">login url</a>' % (reverse('login_view'), request.path))
    logout_url = mark_safe('<a href="%s?next=%s">logout url</a>' % (reverse('logout'), request.path))
    
    c = Context({'user' : request.user,
                 'login_url' : login_url,
                 'logout_url' : logout_url})
    t = loader.get_template('unprotected_view.html')

    return HttpResponse(t.render(c))