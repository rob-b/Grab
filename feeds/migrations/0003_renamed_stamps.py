from south.db import db
from feeds.models import Post, Feed
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Migration:

    def forwards(self):
        db.rename_column(Feed._meta.db_table, 'last_modified', 'updated')
        db.rename_column(Post._meta.db_table, 'date_modified', 'updated')
        db.rename_column(Post._meta.db_table, 'date_created', 'created')

    def backwards(self):
        db.rename_column(Feed._meta.db_table, 'updated', 'last_modified')
        db.rename_column(Post._meta.db_table, 'updated', 'date_modified')
        db.rename_column(Post._meta.db_table, 'created', 'date_created')
