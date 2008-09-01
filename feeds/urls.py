from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

from feeds.views import feed_list, feed_detail
from feeds.models import Feed

feed_dict = {
    'queryset': Feed.objects.all(),
    'template_name': 'grab/feed_detail.html',
    'template_object_name': 'feed',
}

urlpatterns = patterns('',
    url(r'^$', feed_list, name="home"),
    (r'(?P<object_id>[\d]+)/$', object_detail, feed_dict),
    (r'(?P<object_id>[\d]+)/fresh/$', feed_detail),
)
