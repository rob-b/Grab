from haystack import indexes
from haystack import site
from feeds.models import Post

class PostIndex(indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    summary = indexes.CharField(model_attr='summary')
    link = indexes.CharField(model_attr='link')
    rendered = indexes.CharField(use_template=True,
                                 template_name='search/indexes/feeds/post_rendered.html',
                                 indexed=False)

site.register(Post, PostIndex)
