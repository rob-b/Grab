from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'', include('feeds.urls')),
)

from django.conf import settings
if settings.DEBUG:
    MEDIA_URL = settings.MEDIA_URL.strip('/')
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % MEDIA_URL, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),
)
