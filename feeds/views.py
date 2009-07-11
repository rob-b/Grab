from hostel.decorators import rendered
from feeds.models import Feed, Post
from feeds.tools import FeedProcessor
from feeds.forms import FeedForm

from django.shortcuts import get_object_or_404

@rendered
def feed_list(request):
    posts = Post.objects.all()
    return 'feeds/feed_list.html', {'posts': posts}

@rendered
def feed_detail(request, object_id, update=False):
    feed = get_object_or_404(Feed, id=object_id)
    feed_status = False

    if update:
        fp = FeedProcessor(Post)
        feed = fp.process_feed(feed)
        if hasattr(feed, 'status') and feed.status == 304:
            feed_status = "unmodified"
    posts = Post.objects.filter(feed=feed.id)

    data = {
        'feed': feed,
        'posts': posts,
        'feed_status': feed_status,
    }
    return 'feeds/feed_detail.html', data

@rendered
def feed_add(request):

    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedForm()
    return 'feeds/feed_add.html', {'form': form}
