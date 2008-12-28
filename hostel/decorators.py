from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def rendered(func):
    """Decorator to simplify returning RequestContext"""
    def render_function(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse) or isinstance(response,
                                                            HttpResponseRedirect):
            return response
        template_name, items = response
        return render_to_response(template_name, items,
                                  context_instance=RequestContext(request))
    return render_function
