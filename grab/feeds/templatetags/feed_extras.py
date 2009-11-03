from django import template
from urlparse import urlparse
register = template.Library()

@register.simple_tag
def feed_favicon(feed):
    o = urlparse(feed.feed_url)
    url = u'%s%s://%s' % ('http://getfavicon.appspot.com/', o.scheme, o.netloc)
    return url

