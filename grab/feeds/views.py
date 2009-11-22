from hostel.decorators import rendered
from feeds.models import Feed, Post
from feeds.tools import populate_feed
from feeds.forms import FeedForm, ReadForm

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.conf import settings
from datetime import datetime
from django.core import serializers
import beanstalkc

@rendered
def feed_list(request, all_posts=False):
    posts = Post.objects.unread() if not all_posts else Post.objects.all()
    return 'feeds/feed_list.html', {
        'posts': posts,
        'form': ReadForm(),
    }

@rendered
def feed_detail(request, slug, update=False, all_posts=False):
    feed = get_object_or_404(Feed, slug=slug)
    feed_status = False

    delta = datetime.now() - feed.last_checked
    if update or delta.seconds / 60 > getattr(settings, 'FEED_UPDATE_TIME', 15):
        beanstalk = beanstalkc.Connection()
        beanstalk.put(str(slug))
    #     new_posts = list(populate_feed(feed))
    #     return HttpResponseRedirect(reverse('feed_detail', args=[slug]))
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

@require_POST
def post_read(request, object_id, read=True):
    dest = request.META.get('HTTP_REFERER')
    try:
        post = Post.objects.get(pk=object_id)
    except Post.DoesNotExist:
        assert False, 'What should i do?'
    post.read = not post.read
    post.save()
    if request.is_ajax():
        return HttpResponse('%s is now %s' % (post, post.read))
    return HttpResponseRedirect(dest)

def post_unread(request, object_id):
    return post_read(request, object_id, False)

@require_POST
def new_items_check(request, slug):
    # try:
    #     feed = Feed.objects.get(slug=slug)
    # except feed.DoesNotExist:
    #     assert False, 'What should i do?'
    # posts = populate_feed(feed)
    posts = Feed.objects.get(slug=slug).post_set.all()[:5]
    data = serializers.serialize('json', posts)
    return HttpResponse(data)


