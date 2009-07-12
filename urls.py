from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('feeds.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',

        (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),)
