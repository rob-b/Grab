from django.conf import settings

def attachment_url(request):
    return {
        'ATTACHMENT_URL': settings.ATTACHMENT_URL,
    }

from functools import wraps
def exclude_admin(admin_path='/admin'):
    """if a decorated context_processor is called on a page the url of which
    begins with admin_path then return an empty dictionary"""
    def decorator(f):
        def wrapper(request):
            if request.get_full_path().startswith(admin_path):
                return {}
            return f(request)
        return wraps(f)(wrapper)
    return decorator
