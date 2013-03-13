from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    c = Context({'user' : request.user})
    t = loader.get_template('index.html')
    return HttpResponse(t.render(c))

@login_required
def protected_view(request):
    profile = ""

    if request.user.is_authenticated():
        profile = request.user.get_profile()

    return HttpResponse("Succesfully seeing a protected view.")
    
def unprotected_view(request):
    return HttpResponse("Succesfully seeing a non-protected view")