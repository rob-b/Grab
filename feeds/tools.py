from django.db import models
import feedparser
from datetime import datetime
import time
import sys
import shelve
from feedcache import cache

def mtime(timetuple):
    modified = list(timetuple[0:8]) + [-1]
    return datetime.fromtimestamp(time.mktime(modified))

def populate_feed(feed_obj):

    # this is not threadsafe and will likely break on a real server
    storage = shelve.open(feed_obj.name)
    fc = cache.Cache(storage)
    item = fc.fetch(feed_obj.feed_url)
    # item = feedparser.parse(feed_obj.feed_url)
    feed_obj.title = item.feed.title
    feed_obj.link = item.feed.link
    feed_obj.etag = item.etag
    feed_obj.tagline = item.feed.tagline
    try:
        feed_obj.updated = mtime(item.modified)
    except AttributeError:
        feed_obj.updated = None
    feed_obj.last_checked = datetime.now()
    for entry in item.entries:
        post = create_post(entry)
        post.feed = feed_obj
        post.save()

def create_post(entry):
    from models import Post
    post = Post()
    for k, v in entry.items():
        try:
            field = post._meta.get_field_by_name(k)[0]
        except models.FieldDoesNotExist:
            continue
        if not isinstance(field, models.AutoField):
            setattr(post, k, v)

    # we cannot be sure of the entry.items order and so we have to setup the
    # datefield handling after initial values have been set. feels unDRY
    for k, v in entry.items():
        if not k.endswith('_parsed'):
            continue
        name = k.replace('_parsed', '')
        try:
            field = post._meta.get_field_by_name(name)[0]
        except models.FieldDoesNotExist:
            continue
        if hasattr(post, name) and isinstance(field, models.DateTimeField):
            setattr(post, name, mtime(v))
    return post

# old, possibly useless code
class FeedProcessor(object):

    def __init__(self, Post):
        self.Post = Post

    def process_feed(self, stored_feed):
        if not stored_feed.post_set.all():
            etag = modified = None
        else:
            etag = stored_feed.etag
            try:
                modified = stored_feed.last_modified.timetuple()
            except:
                modified = None
        try:
            feed = feedparser.parse(stored_feed.feed_url,
                                    etag=etag,
                                    modified=modified,)
        except:
            raise

        if hasattr(feed, 'status'):
            if feed.status == 304:
                return stored_feed
            if feed.status >= 400:
                return False

        if hasattr(feed, 'modified'):
            stored_feed.last_modified = mtime(feed.modified)
        else:
            stored_feed.last_modified = datetime.now()
        stored_feed.title = feed.get('title', '')
        stored_feed.tagline = feed.get('tagline', '')
        stored_feed.link = feed.get('link','')
        stored_feed.last_checked = datetime.now()
        stored_feed.save()

        guids = []
        for entry in feed.entries:

            if hasattr(entry, 'id') and entry.id:
                guids.append(entry.id)
            elif entry.title:
                guids.append(entry.title)
            elif entry.link:
                guids.append(entry.link)
        if guids:
            postdict = dict([(post.guid, post)
                             for post in self.Post.objects.filter(
                                 feed=stored_feed.id).filter(guid__in=guids)])
        else:
            postdict ={}

        for entry in feed.entries:
            self.process_entry(stored_feed, entry, postdict)
        return stored_feed

    def process_all_entries(self, feed):
        for entry in feed.entries:
            process_entry(feed, entry)
        return stored_feed

    def process_entry(self, feed, entry, postdict):

        link = entry.link if 'link' in entry else feed.link
        try:
            item, created = self.Post.objects.get_or_create(link=link,
                                                            defaults={'feed':feed})
        except Exception, e:
            print link, feed
            raise
        item.link = link
        item.title = entry.title if 'title' in entry else feed.link
        item.guid = entry.id if 'id' in entry else feed.link

        try:
            item.content = entry.content[0].value
        except:
            item.content = entry.get('summary', entry.get('description'))

        if 'modified_parsed' in entry:
            item.updated = mtime(entry['modified_parsed'])

        if 'author_detail' in entry:
            item.author = entry.author_detail.get('name', '')
            item.author_email = entry.author_detail.get('email','')
        item.feed = feed
        item.save()
