from utils.helpers import rendered
from feeds.models import Feed, Post
from feeds.tools import process_feed

@rendered
def feed_list(request):

    feeds = Feed.objects.all()
    return 'grab/feed_list.html', {'feeds': feeds}

@rendered
def feed_detail(request, object_id):
    feed = Feed.objects.get(id=object_id)
    process_feed(feed)
    posts = Post.objects.filter(feed=feed.id)
    return 'grab/feed_detail.html', {'feed': feed, 'posts': posts}
