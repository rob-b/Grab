from django.db import IntegrityError
from django.db import models
from django.db.models import SlugField
from django.template.defaultfilters import slugify
from django.utils.html import escape
from django.utils.safestring import mark_safe

from hostel.utils.html import purify_markdown
import markdown

class AutoSlugField (SlugField):
    """
    A SlugField that automatically populates itself at save-time from
    the value of another field.

    Uses the first field listed in prepopulate_from as the field to
    populate from at save time.  If prepopulate_from is not set, looks
    for populate_from, which should be the name of a single field (not
    a tuple or list).

    By default, also sets unique=True, db_index=True, and
    editable=False.

    Accepts additional argument, overwrite_on_save.  If True, will
    re-populate on every save, overwriting any existing value.  If
    False, will not touch existing value and will only populate if
    slug field is empty.  Default is False.

    """
    def __init__ (self, *args, **kwargs):
        kwargs.setdefault('unique', True)
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('editable', False)
        self._save_populate = kwargs.get('prepopulate_from', [None])[0]
        if self._save_populate is None:
            self._save_populate = kwargs.pop('populate_from', None)
        self._overwrite_on_save = kwargs.pop('overwrite_on_save', False)
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def _populate_slug(self, model_instance):
        value = getattr(model_instance, self.attname, None)
        prepop = getattr(model_instance, self._save_populate, None)
        if (prepop is not None) and (not value or self._overwrite_on_save):
            value = slugify(prepop)
            setattr(model_instance, self.attname, value)
        return value

    def contribute_to_class (self, cls, name):
        cls._orig_save = cls.save
        def save (self_, *args, **kwargs):
            counter = 1
            orig_slug = self._populate_slug(self_)
            slug_len = len(orig_slug)
            if slug_len > self.max_length:
                orig_slug = orig_slug[:self.max_length]
                slug_len = self.max_length
            setattr(self_, name, orig_slug)
            while True:
                try:
                    self_._orig_save(*args, **kwargs)
                    break
                except IntegrityError, e:
                    # check to be sure a slug fight caused the IntegrityError
                    s_e = str(e).lower()
                    if (name in s_e or getattr(self_, name) in s_e) and ('duplicate' in s_e or 'unique' in s_e):
                        counter += 1
                        max_len = self.max_length - (len(str(counter)) + 1)
                        if slug_len > max_len:
                            orig_slug = orig_slug[:max_len]
                        new_slug = "%s-%s" % (orig_slug, counter)
                        setattr(self_, name, new_slug.replace('--', '-'))
                    else:
                        raise
        cls.save = save
        super(AutoSlugField, self).contribute_to_class(cls, name)

_field_name = lambda name: '%s_rendered' % name
class MarkdownField(models.TextField):

    def __init__(self, *args, **kwargs):

        self.whitelist = kwargs.pop('whitelist', None)
        self.attr_whitelist = kwargs.pop('attr_whitelist', None)
        self.blacklist = kwargs.pop('blacklist', None)
        self.attributes_with_urls = kwargs.pop('attributes_with_urls', None)
        super(MarkdownField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        field_name = '%s_rendered' % name
        field_as_html_name = '%s_html' % name
        field = models.TextField(editable=False)
        cls.add_to_class(field_name, field)
        super(MarkdownField, self).contribute_to_class(cls, name)

        def as_html(self):
            return mark_safe(getattr(self, field_name))
        cls.add_to_class(field_as_html_name, property(as_html))

    def pre_save(self, model_instance, add):
        markup = getattr(model_instance, self.attname)

        rendered = markdown.markdown(markup, safe_mode='remove')
        rendered= purify_markdown(rendered, self.whitelist,
                                   self.attr_whitelist, self.blacklist,
                                   self.attributes_with_urls)
        setattr(model_instance, _field_name(self.attname), rendered)
        return markup
