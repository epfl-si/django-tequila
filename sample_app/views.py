from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render


def index(request):
    user_info = request.user.__dict__
    user_info.update(request.user.profile.__dict__)

    return render(request, 'index.html', {
        'user' : request.user,
        'user_info': user_info,
    })


@login_required
def protected_view(request):
    profile = ""

    if request.user.is_authenticated():
        profile = request.user.profile

    return HttpResponse("Successfully seeing a protected view.")


def unprotected_view(request):
    login_url = mark_safe('<a href="%s?next=%s">login url</a>' % (reverse('login_view'), request.path))
    logout_url = mark_safe('<a href="%s?next=%s">logout url</a>' % (reverse('logout'), request.path))

    context = {'user' : request.user,
               'logout_url' : logout_url}

    return render(request, 'unprotected_view.html', context)
