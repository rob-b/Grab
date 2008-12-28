
from south.db import db
from feeds.models import *
from django.utils.translation import ugettext_lazy as _

class Migration:
    
    def forwards(self):
        
        # Model 'Site'
        db.create_table('feeds_site', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(_('name'), max_length=100)),
            ('url', models.URLField(_('url'), verify_exists=False, unique=True, help_text=_('e.g. http://example.com'),)),
            ('description', models.TextField(_('description')))
        ))
        # Model 'Feed'
        db.create_table('feeds_feed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed_url', models.URLField(_('feed url'), unique=True)),
            ('name', models.CharField(_('name'), max_length=100)),
            ('is_active', models.BooleanField(_('is active'), default=True, help_text=_('If disabled, this feed will\ not be further updated.'))),
            ('title', models.CharField(_('title'), max_length=200, blank=True)),
            ('tagline', models.TextField(_('tagline'), blank=True)),
            ('link', models.URLField(_('link'), blank=True)),
            ('etag', models.CharField(_('etag'), max_length=50, blank=True, null=True)),
            ('last_modified', models.DateTimeField(_('last modified'), null=True, blank=True)),
            ('last_checked', models.DateTimeField(_('last checked'), null=True, blank=True))
        ))
        # Mock Models
        Feed = db.mock_model(model_name='Feed', db_table='feeds_feed', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField)
        
        # Model 'Post'
        db.create_table('feeds_post', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(Feed, verbose_name=_('feed'), null=False, blank=False)),
            ('title', models.CharField(_('title'), max_length=255)),
            ('link', models.URLField(_('link'), )),
            ('content', models.TextField(_('content'), blank=True)),
            ('date_modified', models.DateTimeField(_('date modified'), null=True, blank=True)),
            ('guid', models.CharField(_('guid'), max_length=200, db_index=True)),
            ('author', models.CharField(_('author'), max_length=50, blank=True)),
            ('author_email', models.EmailField(_('author email'), blank=True)),
            ('comments', models.URLField(_('comments'), blank=True)),
            ('date_created', models.DateField(_('date created'), auto_now_add=True))
        ))
        db.create_index('feeds_post', ['feed_id','guid'], unique=True, db_tablespace='')
        
        
        db.send_create_signal('feeds', ['Site','Feed','Post'])
    
    def backwards(self):
        
        db.delete_table('feeds_site')
        db.delete_table('feeds_feed')
        db.delete_table('feeds_post')
