from BeautifulSoup import BeautifulSoup
import re


WHITELIST = ['blockquote', 'em', 'i', 'img', 'strong', 'u', 'a', 'b', "p", "br", "code", "pre" ]
ATTR_WHITELIST = { 'a':['href','title','hreflang'], 'img':['src', 'width', 'height', 'alt', 'title'] }
BLACKLIST = [ 'script', 'style' ]
ATTRIBUTES_WITH_URLS = [ 'href', 'src' ]

def purify_markdown(untrusted_html, whitelist=None, attr_whitelist=None,
                    blacklist=None, attributes_with_urls=None,
                    replacement_tag='p'):

    """
    Remove undesired elements from markdown generated html.
    We sort of assume that the markdown option to strip html has been used and
    so there is nothing but valid html

    based on http://jerakeen.org/blog/2008/05/sanitizing-comments-with-python/
    """
    whitelist = whitelist or WHITELIST
    attr_whitelist = attr_whitelist or ATTR_WHITELIST
    blacklist = blacklist or BLACKLIST
    attributes_with_urls = attributes_with_urls or ATTRIBUTES_WITH_URLS

    # BeautifulSoup is catching out-of-order and unclosed tags, so markup
    # can't leak out of comments and break the rest of the page.
    soup = BeautifulSoup(untrusted_html)

    # now strip HTML we don't like.
    for tag in soup.findAll():
        if tag.name.lower() in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()
        elif tag.name.lower() in whitelist:
            # tag is allowed. Make sure all the attributes are allowed.
            for attr in tag.attrs:
                # allowed attributes are whitelisted per-tag
                if tag.name.lower() in attr_whitelist and attr[0].lower() in attr_whitelist[ tag.name.lower() ]:
                    # some attributes contain urls..
                    if attr[0].lower() in attributes_with_urls:
                        # ..make sure they're nice urls
                        if not re.match(r'(https?|ftp)://', attr[1].lower()):
                            tag.attrs.remove( attr )

                    # ok, then
                    pass
                else:
                    # not a whitelisted attribute. Remove it.
                    tag.attrs.remove( attr )
        else:
            # not a whitelisted tag. I'd like to remove it from the tree
            # and replace it with its children. But that's hard. It's much
            # easier to just replace it with an empty span tag.
            tag.name = replacement_tag
            tag.attrs = []

    # stringify back again
    safe_html = unicode(soup)

    # HTML comments can contain executable scripts, depending on the browser, so we'll  
    # be paranoid and just get rid of all of them  
    # e.g. <!--[if lt IE 7]><script type="text/javascript">h4x0r();</script><![endif]-->  
    # TODO - I rather suspect that this is the weakest part of the operation..
    safe_html = re.sub(r'<!--[.\n]*?-->','',safe_html)
    return safe_html

