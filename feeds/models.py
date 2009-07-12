from django.db import models
from django.utils.translation import ugettext_lazy as _

from tools import populate_feed
import feedparser


class Site(models.Model):
    name = models.CharField(_('name'), max_length=100)
    url = models.URLField(_('url'),
                          verify_exists=False,
                          unique=True,
                          help_text=_('e.g. http://example.com'),)
    description = models.TextField(_('description'))

    class Meta:
        verbose_name = _('site')
        verbose_name_plural = _('sites')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name


class FeedManager(models.Manager):
    pass

class Feed(models.Model):
    feed_url = models.URLField(_('feed url'), unique=True)

    name = models.CharField(_('name'), max_length=100)
    is_active = models.BooleanField(_('is active'),
                                    default=True,
                                    help_text=_('If disabled, this feed will\
                                                not be further updated.'))

    title = models.CharField(_('title'), max_length=200, blank=True)
    tagline = models.TextField(_('tagline'), blank=True)
    link = models.URLField(_('link'), blank=True)

    # http://feedparser.org/docs/http-etag.html
    etag = models.CharField(_('etag'), max_length=50, blank=True, null=True)
    updated = models.DateTimeField(_('last modified'), null=True, blank=True)
    last_checked = models.DateTimeField(_('last checked'), null=True, blank=True)

    # manager
    objects = FeedManager()

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        ordering = ('name', 'feed_url',)

    def __unicode__(self):
        return u'%s' % (self.name,)

    @models.permalink
    def get_absolute_url(self):
        return ('feed_detail', str(self.id))

class Post(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('feed'))
    title = models.CharField(_('title'), max_length=255)
    link = models.URLField(_('link'), )
    summary = models.TextField(_('summary'), blank=True)
    content = models.TextField(_('content'), blank=True)
    author = models.CharField(_('author'), max_length=255, blank=True)
    author_email = models.EmailField(_('author email'), blank=True)
    created = models.DateField(_('date created'), auto_now_add=True)
    updated = models.DateTimeField(_('date modified'), null=True, blank=True)
    read = models.BooleanField(_('has this post been read'), default=False)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-updated',)
        unique_together = (('feed', 'link'),)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link

    @property
    def get_content(self):
        return self.content or self.summary

# signals
def feed_creation(sender, **kwargs):
    if kwargs.get('created'):
        populate_feed(kwargs['instance'])
models.signals.post_save.connect(feed_creation, sender=Feed)
