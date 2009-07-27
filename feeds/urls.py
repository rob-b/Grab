from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

from feeds.views import feed_list, feed_detail, feed_add
from feeds.models import Feed

feed_dict = {
    'queryset': Feed.objects.all(),
    'template_name': 'feeds/feed_detail.html',
    'template_object_name': 'feed',
}

urlpatterns = patterns('feeds.views',
    url(r'^$', 'feed_list', name="home"),
    url(r'^all/$', 'feed_list', {'all_posts': True}, name="feeds_home_all"),

    url(r'^(?P<object_id>[\d]+)/$', 'feed_detail', name="feed_detail"),
    url(r'^(?P<object_id>[\d]+)/all/$',
        'feed_detail',
        {'all_posts': True},
        name="feed_detail_all"),
    (r'(?P<object_id>[\d]+)/fresh/$',
     'feed_detail',
     {'update':True}),

    url(r'^add/$', feed_add, name='feed_add'),
    url(r'^read/(?P<object_id>\d+)/$',
        'post_read',
        name='feeds_post_read'),
    url(r'^unread/(?P<object_id>\d+)/$',
        'post_unread',
        name='feeds_post_unread'),
)
