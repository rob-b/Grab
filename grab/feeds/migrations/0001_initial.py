
from south.db import db
from django.db import models
from feeds.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('id', models.AutoField(primary_key=True)),
            ('feed_url', models.URLField(_('feed url'), unique=True)),
            ('name', models.CharField(_('name'), max_length=100)),
            ('is_active', models.BooleanField(_('is active'), default=True)),
            ('title', models.CharField(_('title'), max_length=200, blank=True)),
            ('tagline', models.TextField(_('tagline'), blank=True)),
            ('link', models.URLField(_('link'), max_length=255, blank=True)),
            ('etag', models.CharField(_('etag'), max_length=50, null=True, blank=True)),
            ('updated', models.DateTimeField(_('last modified'), null=True, blank=True)),
            ('last_checked', models.DateTimeField(_('last checked'), null=True, blank=True)),
        ))
        db.send_create_signal('feeds', ['Feed'])
        
        # Adding model 'Post'
        db.create_table('feeds_post', (
            ('id', models.AutoField(primary_key=True)),
            ('feed', models.ForeignKey(orm.Feed)),
            ('title', models.CharField(_('title'), max_length=255)),
            ('link', models.URLField(_('link'), max_length=255)),
            ('summary', models.TextField(_('summary'), blank=True)),
            ('content', models.TextField(_('content'), blank=True)),
            ('author', models.CharField(_('author'), max_length=255, blank=True)),
            ('author_email', models.EmailField(_('author email'), blank=True)),
            ('created', models.DateField(_('date created'), auto_now_add=True)),
            ('updated', models.DateTimeField(_('date modified'), null=True, blank=True)),
            ('read', models.BooleanField(_('has this post been read'), default=False)),
        ))
        db.send_create_signal('feeds', ['Post'])
        
        # Adding model 'Site'
        db.create_table('feeds_site', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(_('name'), max_length=100)),
            ('url', models.URLField(_('url'), unique=True, verify_exists=False)),
            ('description', models.TextField(_('description'))),
        ))
        db.send_create_signal('feeds', ['Site'])
        
        # Creating unique_together for [feed, link] on Post.
        db.create_unique('feeds_post', ['feed_id', 'link'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')
        
        # Deleting model 'Post'
        db.delete_table('feeds_post')
        
        # Deleting model 'Site'
        db.delete_table('feeds_site')
        
        # Deleting unique_together for [feed, link] on Post.
        db.delete_unique('feeds_post', ['feed_id', 'link'])
        
    
    
    models = {
        'feeds.feed': {
            'Meta': {'ordering': "('name','feed_url',)"},
            'etag': ('models.CharField', ["_('etag')"], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'feed_url': ('models.URLField', ["_('feed url')"], {'unique': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('models.BooleanField', ["_('is active')"], {'default': 'True'}),
            'last_checked': ('models.DateTimeField', ["_('last checked')"], {'null': 'True', 'blank': 'True'}),
            'link': ('models.URLField', ["_('link')"], {'max_length': '255', 'blank': 'True'}),
            'name': ('models.CharField', ["_('name')"], {'max_length': '100'}),
            'tagline': ('models.TextField', ["_('tagline')"], {'blank': 'True'}),
            'title': ('models.CharField', ["_('title')"], {'max_length': '200', 'blank': 'True'}),
            'updated': ('models.DateTimeField', ["_('last modified')"], {'null': 'True', 'blank': 'True'})
        },
        'feeds.post': {
            'Meta': {'ordering': "('-updated',)", 'unique_together': "(('feed','link'),)", 'get_latest_by': "'created'"},
            'author': ('models.CharField', ["_('author')"], {'max_length': '255', 'blank': 'True'}),
            'author_email': ('models.EmailField', ["_('author email')"], {'blank': 'True'}),
            'content': ('models.TextField', ["_('content')"], {'blank': 'True'}),
            'created': ('models.DateField', ["_('date created')"], {'auto_now_add': 'True'}),
            'feed': ('models.ForeignKey', ["orm['feeds.Feed']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'link': ('models.URLField', ["_('link')"], {'max_length': '255'}),
            'read': ('models.BooleanField', ["_('has this post been read')"], {'default': 'False'}),
            'summary': ('models.TextField', ["_('summary')"], {'blank': 'True'}),
            'title': ('models.CharField', ["_('title')"], {'max_length': '255'}),
            'updated': ('models.DateTimeField', ["_('date modified')"], {'null': 'True', 'blank': 'True'})
        },
        'feeds.site': {
            'Meta': {'ordering': "('name',)"},
            'description': ('models.TextField', ["_('description')"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('name')"], {'max_length': '100'}),
            'url': ('models.URLField', ["_('url')"], {'unique': 'True', 'verify_exists': 'False'})
        }
    }
    
    complete_apps = ['feeds']
