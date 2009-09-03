from lxml import etree
from lxml.html import fromstring
from lxml.html.clean import Cleaner
from itertools import chain

def kill_guardian_tracking(kwargs):
    summary = kwargs['summary']
    html = fromstring(summary)

    # first get rid of doubleclick links
    elems = [el for el in html.getchildren() if el.find('a') is not None]
    links = list(chain(*[elem.findall('a') for elem in elems]))
    for link in links:
        try:
            if 'doubleclick' in link.attrib['href']:
                link.getparent().remove(link)
        except KeyError:
            pass

    # remove the tracking div
    try:
        divs = [div for div in html.findall('div') if 'track' in
                div.attrib['class']]
    except KeyError:
        pass
    else:
        for div in divs:
            div.getparent().remove(div)

    # perhaps at some point it would be worth using cleaner on the html
    # cleaner = Cleaner(style=True)
    # kwargs['summary'] = cleaner.clean_html(etree.tostring(html))
    kwargs['summary'] = etree.tostring(html)
    return kwargs
