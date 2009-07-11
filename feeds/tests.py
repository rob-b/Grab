from django.test import TestCase
from models import Feed, Post
from models import create_post

import shelve
from feedcache import cache
import feedparser

class FeedTests(TestCase):

    def setUp(self):
        storage = shelve.open('feedlearning')
        fc = cache.Cache(storage)
        self.feed = fc.fetch('http://reddit.com/r/django.rss')

    def test_post_creation(self):
        posts = []
        for entry in self.feed.entries:
            posts.append(create_post(entry))

