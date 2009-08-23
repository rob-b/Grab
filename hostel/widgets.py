"""
Extra HTML Widget classes
"""

import datetime
import re

from django.forms.widgets import Widget, Select, FileInput
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _ 

__all__ = ('SelectDateWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        if years:
            self.years = years
            self.years.reverse()
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year+10)
            self.years.reverse()

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = MONTHS.items()
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        select_html = Select(choices=month_choices).render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        day_choices = [(i, i) for i in range(1, 32)]
        local_attrs['id'] = self.day_field % id_
        select_html = Select(choices=day_choices).render(self.day_field % name, day_val, local_attrs)
        output.append(select_html)

        # if later on they decide that they do want this order swapped then just
        # uncomment this line
        # output[0], output[1] = output[1], output[0]

        year_choices = [(i, i) for i in self.years]
        local_attrs['id'] = self.year_field % id_
        select_html = Select(choices=year_choices).render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y, m, d = data.get(self.year_field % name), data.get(self.month_field % name), data.get(self.day_field % name)
        if y and m and d:
            return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)


class ImageWidget(FileInput):
    """
    Renders the input field and a thumbnail
    """

    def render(self, name, value, attrs=None):
        return u''


class AdminReadOnlyFileWidget(AdminFileWidget):
    """
    Renders a file widget without input
    """

    def __init__(self, attrs=None):
        super(AdminReadOnlyFileWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('%s <a target="_blank" href="%s">%s</a>' % (_('Currently:'), value.url, value))
            # output.append(super(AdminFileWidget, self).render(name, value, attrs))
            return mark_safe(u''.join(output))
        return mark_safe(_('No file attached'))
