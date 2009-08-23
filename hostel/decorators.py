from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.exceptions import PermissionDenied

from functools import update_wrapper, wraps
import markdown
import re

def rendered(func):
    """Decorator to simplify returning RequestContext"""
    @wraps(func)
    def render_function(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse) or isinstance(response,
                                                            HttpResponseRedirect):
            return response
        template_name, items = response
        return render_to_response(template_name, items,
                                  context_instance=RequestContext(request))
    return render_function

def detect_cookies(f):
    """The auth.views.login knows enough to test for cookies but doesn't
    actually do so. A little shove to help out"""
    def wrapper(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):

        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = RequestSite(request)

        if request.method == 'POST':

            # sometimes we won't have made a get request yet (i.e. if we use a
            # form on a different page to login) so if the referer was
            # from our own site skip the cookie check
            referer = request.META.get('HTTP_REFERER', None)
            try:
                referer = referer.split(u'//')[1]
            except AttributeError:
                referer = ''
            cookies = request.session.test_cookie_worked()
            form = AuthenticationForm(request, request.POST)
            form.is_valid()
        else:
            cookies = True
            form = AuthenticationForm(request.POST)

        request.session.set_test_cookie()
        if cookies or referer.startswith(current_site.domain):
            request.session.delete_test_cookie()
            return f(request, template_name, redirect_field_name)

        return render_to_response(template_name, {
            'form': form,
            redirect_field_name: redirect_field_name,
            'site_name': current_site.name,
        }, context_instance=RequestContext(request))
    return update_wrapper(wrapper, f)

def add_markdown(func, suffix='_markdown'):
    """Decorates the save method of a model with markdown fields.

    Assumes the model has fields like:
        body = model.TextField()
        body_markdown = model.TextField()
    where the markdown content is entered into the body_markdown field and then
    on saving an html version is saved to the body field. will automatically
    populate all fields that have a corresponding _markdown field with the html
    version of that _markdown field"""

    re_suffix = r'[\w]+%s$' % suffix
    re_suffix = re.compile(re_suffix)
    def save_markdown(self, *args, **kwargs):
        for field in self._meta.get_all_field_names():
            match = re_suffix.match(field)
            if match and hasattr(self, field.replace(suffix, '')):
                md = markdown.Markdown(safe_mode='remove')
                value = md.convert(getattr(self, field))
                setattr(self, field.replace(suffix, ''), value)
        return func(self, *args, **kwargs)
    return update_wrapper(save_markdown, func)

def access_allowed(test_func, redirect_url=None):
    """
    decorate views by making sure that passes a test function that will then
    allow them access to that view. test_func must be a callable that takes a
    user instance as it's only argument and returns a boolean.

    This differs from django.contrib.auth.decorators.user_passes_test in that
    this does not push users who fail the test to a login page
    """
    def decorate(view_func):
        def wrapper(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return update_wrapper(wrapper, view_func)
    return decorate

def redirect_to_profile(f):
    def wrapper(request, **kwargs):
        response = f(request, **kwargs)
        if isinstance(response, HttpResponseRedirect) and \
           request.user.is_authenticated():
            if 'next' in request.GET:
                destination = request.GET['next']
            else:
                profile = request.user.get_profile()
                destination = profile.get_absolute_url()
            return HttpResponseRedirect(destination)
        return response
    return update_wrapper(wrapper, f)


def set_language(f):
    from django.utils import translation
    def wrapper(*args, **kwargs):
        language = translation.get_language()
        translation.activate(language)
        return f(*args, **kwargs)
    return update_wrapper(wrapper, f)

