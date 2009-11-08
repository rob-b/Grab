from django.test import TestCase
from models import Feed, Post
from tools import entry_to_post_args

import shelve
import os.path
from feedcache import cache

class FeedTests(TestCase):

    def setUp(self):
        self.storage = shelve.open(os.path.join('./cache', 'testfeed.cache'))
        fc = cache.Cache(self.storage)
        self.feed = fc.fetch('http://www.reddit.com/r/django.rss',
                             offline=True)
        if self.feed is None:
            self.feed = fc.fetch('http://www.reddit.com/r/django.rss')


    def tearDown(self):
        self.storage.close()

    def test_post_creation(self):
        posts = []
        for entry in self.feed.entries:
            post = Post(**entry_to_post_args(entry))
            posts.append(post)

    def test_create_feed(self):
        feed = Feed()
        feed.feed_url = 'http://www.reddit.com/r/django.rss'
        feed.name = 'Django Reddit'
        feed.save()

    # def test_feed_update(self):
    #     feed = Feed()
    #     feed.feed_url = 'http://feeds.guardian.co.uk/theguardian/rss'
    #     feed.name = 'Guardian'
    #     feed.save()
    #     self.assert_(len(Post.objects.filter(feed__feed_url=feed.feed_url)) > 0)

    #     dest = feed.get_absolute_url() + 'fresh/'
    #     response = self.client.get(dest)

