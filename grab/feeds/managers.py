from django.db import models

class PostManager(models.Manager):

    def unread(self):
        return self.filter(read=False)
