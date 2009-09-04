from hostel.decorators import rendered
from feeds.models import Feed, Post
from feeds.tools import FeedProcessor
from feeds.tools import populate_feed
from feeds.forms import FeedForm, ReadForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse

@rendered
def feed_list(request, all_posts=False):
    posts = Post.objects.unread() if not all_posts else Post.objects.all()
    return 'feeds/feed_list.html', {
        'posts': posts,
        'form': ReadForm(),
    }

@rendered
def feed_detail(request, object_id, update=False, all_posts=False):
    feed = get_object_or_404(Feed, id=object_id)
    feed_status = False

    if update:
        populate_feed(feed)
        return HttpResponseRedirect(reverse('feed_detail', args=[object_id]))
    if not all_posts:
        posts = Post.objects.unread().filter(feed=feed.id)
    else:
        posts = Post.objects.all().filter(feed=feed.id)

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
@require_POST
def post_read(request, object_id, read=True):
    dest = request.META.get('HTTP_REFERER')
    try:
        post = Post.objects.get(pk=object_id)
    except Post.DoesNotExist:
        assert False, 'What should i do?'
    post.read = not post.read
    post.save()
    return HttpResponseRedirect(dest)

def post_unread(request, object_id):
    return post_read(request, object_id, False)
