from django.contrib.sites.models import Site, RequestSite
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.translation import check_for_language

def redirect_to_market(request, market):

    # regardless of how they arrived here we can redirect the user to the
    # requested site.
    site = get_object_or_404(Site, domain__istartswith=market)
    dest = request.META.get('HTTP_REFERER', None)
    if dest:
        dest = dest.replace(RequestSite(request).domain, site.domain)
    else:
        dest = site.domain
    Site.objects.clear_cache()
    response = HttpResponseRedirect(dest)

    # setting the language on the other hand can only be done via a post request
    if request.method == 'POST':
        lang_code = market.split('.')[-1]
        if check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
def form_kwargs(request, kwargs=None):
    """djangosnippets.org/snippets/1420"""
    if kwargs is None:
        kwargs ={}
    if request.method == 'POST':
        kwargs['data'] = request.POST
        kwargs['files'] = request.FILES
    return kwargs
