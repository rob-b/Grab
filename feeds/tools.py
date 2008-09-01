import feedparser
from feeds.models import Post
from datetime import datetime
import time
import sys

def mtime(timetuple):

    modified = list(timetuple[0:8]) + [-1]
    return datetime.fromtimestamp(time.mktime(modified))

def process_feed(stored_feed):
    try:
        feed = feedparser.parse(stored_feed.feed_url,
                                etag=stored_feed.etag,
                                modified=stored_feed.last_modified.timetuple())
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

        if entry.id:
            guids.append(entry.id)
        elif entry.title:
            guids.append(entry.title)
        elif entry.link:
            guids.append(entry.link)
    if guids:
        postdict = dict([(post.guid, post)
                         for post in Post.objects.filter(
                             feed=stored_feed.id).filter(guid__in=guids)])
    else:
        postdict ={}

    for entry in feed.entries:
        process_entry(stored_feed, entry, postdict)
    return stored_feed

def process_entry(feed, entry, postdict):

    item = Post()
    item.link = entry.link if 'link' in entry else feed.link
    item.title = entry.title if 'title' in entry else feed.link
    item.guid = entry.id if 'id' in entry else feed.link
    item.feed = feed
    item.save()
