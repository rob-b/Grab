from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.views.decorators.cache import never_cache
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib.auth.decorators import user_passes_test

from hostel.forms import AuthenticationForm, LoginAsForm
from hostel.decorators import rendered

def login(request,
          template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          form_class=AuthenticationForm):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = form_class(data=request.POST, request=request)
        if form.is_valid():
            store_cookie = form.cleaned_data.get('store_login', None)
            if not store_cookie:
                request.session.set_expiry(0)
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return HttpResponseRedirect(redirect_to)
    else:
        form = form_class(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

login = never_cache(login)

def forbidden(request, template_name='403.html'):
    response = render_to_response(template_name,
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response


@user_passes_test(lambda u: u.is_superuser)
@rendered
def login_as(request, username, template_name='login_as.html'):

    qs=User.objects.filter(username=username)
    if request.method == 'POST':
        form = LoginAsForm(request.POST, request=request, qs=qs)
        if form.is_valid():
            form.save()
    else:
        form = LoginAsForm(request=request, qs=qs)
    return template_name, {'form': form}

def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name)
    c = RequestContext(request)
    return HttpResponseServerError(t.render(c))
