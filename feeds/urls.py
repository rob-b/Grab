from django.conf.urls.defaults import *

from feeds.views import feed_list

urlpatterns = patterns('',
    (r'', feed_list),
)
