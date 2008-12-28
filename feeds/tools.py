import feedparser
from datetime import datetime
import time
import sys

def mtime(timetuple):

    modified = list(timetuple[0:8]) + [-1]
    return datetime.fromtimestamp(time.mktime(modified))

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

            if entry.id:
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
        item, created = self.Post.objects.get_or_create(link=link,
                                                        defaults={'feed':feed})
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
