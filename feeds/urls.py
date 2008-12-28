from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

from feeds.views import feed_list, feed_detail, feed_add
from feeds.models import Feed

feed_dict = {
    'queryset': Feed.objects.all(),
    'template_name': 'grab/feed_detail.html',
    'template_object_name': 'feed',
}

urlpatterns = patterns('',
    url(r'^$', feed_list, name="home"),
    url(r'^(?P<object_id>[\d]+)/$', feed_detail, name="feed_detail"),
    (r'(?P<object_id>[\d]+)/fresh/$',
     feed_detail,
     {'update':True}),

    url(r'^add/$', feed_add, name='feed_add'),
)
