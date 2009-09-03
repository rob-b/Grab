from django import template
from django.contrib.sites.models import Site
from django.utils.html import mark_safe
import re
register = template.Library()

@register.simple_tag
def active(request, pattern, class_name='active'):
    if re.search(pattern, request.path):
        return class_name
    return ''

@register.simple_tag
def current_site():
    return Site.objects.get_current()

@register.filter
@template.defaultfilters.stringfilter
def urlquote_plus(value):
    from django.utils.http import urlquote_plus
    return urlquote_plus(value)
urlquote_plus.is_safe = False

def do_ifactive(parser, token):
    """

    """

    end_tag = 'endifactive'

    active_nodes = parser.parse((end_tag,'else'))
    end_token = parser.next_token()
    if end_token.contents == 'else':
        inactive_nodes = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        inactive_nodes = None

    tag_args = token.contents.split(' ')
    if len(tag_args) != 3:
        raise template.TemplateSyntaxError("'%s' takes two arguments"
                                  " (context variable with the request, and path a url)" % tag_args[0])

    request_var = tag_args[1]
    url = tag_args[2]

    return ActiveNode(request_var, url, active_nodes, inactive_nodes)
register.tag('ifactive', do_ifactive)


class ActiveNode(template.Node):

    def __init__(self, request_var, url, active_nodes, inactive_nodes=None):
        self.request_var = request_var
        self.url = url
        self.active_nodes = active_nodes
        self.inactive_nodes = inactive_nodes

    def render(self, context):

        request = template.resolve_variable(self.request_var, context)
        url = template.resolve_variable(self.url, context)

        if url == '/' and request.path == '/':
            return self.active_nodes.render(context)
        match = re.match(url, request.path)
        if match and match.group() != '/':
            return self.active_nodes.render(context)

        if self.inactive_nodes is not None:
            return self.inactive_nodes.render(context)
        return ''


@register.filter
@template.defaultfilters.stringfilter
def truncatestring(src, ln):
    ln = int(ln)
    ret = src[:ln]
    if len(src) > ln:
        ret = ret[:ln-3].strip() + '&hellip;'
    return mark_safe(ret)
truncatestring.is_safe = True

@template.defaultfilters.stringfilter
def to_class(value):
    """Transforms the size into a class"""
    if value:
        value = int(value)
    else:
        value = 1
    if value >= 8:
        size = 'xxl'
    elif value < 8 and value >= 7:
        size = 'xl'
    elif value < 7 and value >= 5:
        size = 'l'
    elif value < 5 and value >= 3:
        size = 'm'
    elif value < 3:
        size = 's'
    return size
register.filter('to_class',to_class)

from django.utils.html import conditional_escape

@register.filter()
def obfuscate(email, linktext=None, vcard=True, autoescape=None):
    """
    Given a string representing an email address,
    returns a mailto link with rot13 JavaScript obfuscation.

    Accepts an optional argument to use as the link text;
    otherwise uses the email address itself.
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    email = re.sub('@','\\\\100', re.sub('\.', '\\\\056', \
        esc(email))).encode('rot13')

    if linktext:
        linktext = esc(linktext).encode('rot13')
    else:
        linktext = email

    if vcard:
        vcard = """ pynff=\\\"rznvy\\\""""
    else:
        vcard = ''

    rotten_link = """<script type="text/javascript">document.write \
        ("<n uers=\\\"znvygb:%s\\\"%s>%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));</script>""" % (email, vcard, linktext)
    return mark_safe(rotten_link)
obfuscate.needs_autoescape = True
