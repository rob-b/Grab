from south.db import db
from feeds.models import Post
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Migration:

    def forwards(self):
        db.add_column(Post._meta.db_table,
                   'read',
                    models.BooleanField(_('has this post been read'),
                                        default=False))

    def backwards(self):
        db.delete_column(Post._meta.db_table, 'read')
