from django.test import TestCase
from models import Feed, Post
from tools import create_post

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


    def test_create_feed(self):
        feed = Feed()
        feed.feed_url = 'http://reddit.com/r/django.rss'
        feed.name = 'Django Reddit'
        feed.save()
