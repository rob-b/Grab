from south.db import db
from feeds.models import Post, Feed
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Migration:

    def forwards(self):
        db.add_column(Post._meta.db_table,
                      'filtered_content',
                      models.TextField(_('content'), blank=True))


    def backwards(self):
        db.delete_column(Post._meta.db_table, 'filtered_content')
