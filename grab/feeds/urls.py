from django.conf.urls.defaults import *

from feeds.views import feed_add
from feeds.models import Feed

feed_dict = {
    'queryset': Feed.objects.all(),
    'template_name': 'feeds/feed_detail.html',
    'template_object_name': 'feed',
}

home = lambda x: redirect('home', permanent=True)
urlpatterns = patterns('',
    url(r'^$', home),
)
urlpatterns += patterns('feeds.views',
    url(r'^all/$', 'feed_list', {'all_posts': True}, name="feeds_home_all"),

    url(r'^add/$', feed_add, name='feed_add'),
    url(r'^read/(?P<object_id>\d+)/$',
        'post_read',
        name='feeds_post_read'),
    url(r'^unread/(?P<object_id>\d+)/$',
        'post_unread',
        name='feeds_post_unread'),

    url(r'^(?P<slug>[-\w]+)/$', 'feed_detail', name="feed_detail"),
    url(r'^(?P<slug>[^/]+)/all/$',
        'feed_detail',
        {'all_posts': True},
        name="feed_detail_all"),
    (r'(?P<slug>[^/]+)/fresh/$',
     'feed_detail',
     {'update':True}),

)
