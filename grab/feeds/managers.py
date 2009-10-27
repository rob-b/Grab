from django.db import models

class PostManager(models.Manager):

    def unread(self):
        return self.filter(read=False)


class FeedManager(models.Manager):
    def get_query_set(self):
        return super(FeedManager, self).get_query_set().filter(
            post__read=False
        ).annotate(unread_posts_count=models.Count('post'))

