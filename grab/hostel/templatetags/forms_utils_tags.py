import re

from django import template

register = template.Library()

CLASS_PATTERN = re.compile(r'\bclass="[\w\d]*"')
VALUE_PATTERN = re.compile(r'\bvalue="[\w\d]*"')

def cssclass(value, arg):
    """
    Replace the attribute css class for Field 'value' with 'arg'.
    http://www.djangosnippets.org/snippets/1586/
    """   
    attrs = value.field.widget.attrs
    orig = attrs['class'] if 'class' in attrs else None
    attrs['class'] = arg
    rendered = str(value)
    if orig:
        attrs['class']
    else:
        del attrs['class']
    return rendered
register.filter('cssclass', cssclass)

def initialvalue(value, arg):
    """
    Replace the initial value for Field 'value' with 'arg'
    """
    value.field.initial = arg
    rendered = str(value)
    return rendered
register.filter('initialvalue', initialvalue)
