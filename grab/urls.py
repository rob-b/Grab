from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'feeds.views.feed_list', name='home'),
    (r'^search/', include('search.urls')),
    (r'^feeds/', include('feeds.urls')),
    (r'^admin/', include(admin.site.urls)),
)


from django.conf import settings
if settings.DEBUG:
    MEDIA_URL = settings.MEDIA_URL.strip('/')
    ATTACHMENT_URL = settings.ATTACHMENT_URL.strip('/')
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % MEDIA_URL, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),
        (r'^%s(?P<path>.*)$' % ATTACHMENT_URL, 'django.views.static.serve',
         {'document_root': settings.ATTACHMENT_ROOT,
          'show_indexes': True}),
)
