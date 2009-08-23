from django.http import HttpResponseForbidden
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import Resolver404

class AuthorizationMiddleware(object):

    def process_response(self, request, response):
        if isinstance(response, HttpResponseForbidden):
            from hostel.views import forbidden
            return forbidden(request)
        else:
            return response


class SetTestCookieMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            request.session.set_test_cookie()


class LoginRequiredMiddleware(object):

    def evaluate_request(self, request):
        from workers import urls as wurls
        from enrollment import urls as eurls
        return False

        urls = list(wurls.urlpatterns) + list(eurls.urlpatterns)
        path = request.path[request.path.find('/', 1):]
        for url in urls:
            try:
                match = url.resolve(path[1:])
                if match:
                    return False
            except Resolver404:
                pass
        allowed = [settings.LOGIN_URL]
        if settings.DEBUG:
            for url in [settings.MEDIA_URL, settings.ATTACHMENT_URL]:
                if request.path.startswith(url):
                    return False

        return request.path not in allowed and request.user.is_anonymous()

    def process_request(self, request):
        if self.evaluate_request(request):
            if request.method == 'POST':
                return login(request)
            else:
                dest = '%s?next=%s' % (settings.LOGIN_URL, request.path)
                return HttpResponseRedirect(dest)
