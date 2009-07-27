from hostel.decorators import rendered
from feeds.models import Feed, Post
from feeds.tools import FeedProcessor
from feeds.tools import populate_feed
from feeds.forms import FeedForm, ReadForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

@rendered
def feed_list(request, all_posts=False):
    posts = Post.objects.unread() if not all_posts else Post.objects.all()
    return 'feeds/feed_list.html', {
        'posts': posts,
        'form': ReadForm(),
    }

@rendered
def feed_detail(request, object_id, update=False):
    feed = get_object_or_404(Feed, id=object_id)
    feed_status = False

    if update:
        populate_feed(feed)
        # fp = FeedProcessor(Post)
        # feed = fp.process_feed(feed)
        # if hasattr(feed, 'status') and feed.status == 304:
        #     feed_status = "unmodified"
    posts = Post.objects.unread().filter(feed=feed.id)

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
            return HttpResponseRedirect(form.instance.get_absolute_url())
    else:
        form = FeedForm()
    return 'feeds/feed_add.html', {'form': form}

@rendered
def post_read(request, object_id):
    try:
        post = Post.objects.get(pk=object_id)
    except Post.DoesNotExist:
        assert False, 'What should i do?'
    post.read = True
    post.save()
    return HttpResponseRedirect(post.feed.get_absolute_url())

