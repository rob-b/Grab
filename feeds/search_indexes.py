from haystack import indexes
from haystack import site
from feeds.models import Post

class PostIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True, indexed=False)
site.register(Post, PostIndex)
