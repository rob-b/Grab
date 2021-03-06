from lxml import etree
from lxml.html import fromstring
from lxml.html import builder as E
from lxml.html import tostring
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
    # from lxml.html.clean import Cleaner
    # cleaner = Cleaner(style=True)
    # kwargs['summary'] = cleaner.clean_html(etree.tostring(html))
    kwargs['summary'] = tostring(html)
    return kwargs

def correct_guardian_lists(kwargs):
    summary = kwargs['summary']
    html = fromstring(summary)

    # get an iterator of all elems with a class
    elems = [elem for elem in html if 'class' in elem.attrib and
             elem.attrib['class'] == 'standfirst']

    for elem in elems:
        bits = [el.strip() for el in elem.text_content().split(u'\u2022') if el]
        ul = E.UL(*[E.LI(bit) for bit in bits])
        html.replace(elem, ul)
    kwargs['summary'] = tostring(html)
    return kwargs
