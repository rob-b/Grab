from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import ugettext_lazy as _
import os

class RestrictedImageField(forms.ImageField):

    """An ImageField that can reject files over a specified size.

    Assumes kilobytes"""

    def __init__(self, max_size=None, *args, **kwargs):
        self.max_size = max_size
        if self.max_size:
            self.max_size *= 1024
        super(RestrictedImageField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        f = super(RestrictedImageField, self).clean(data, initial)
        if self.max_size and data and data.size > self.max_size:
            formatted_size = self.max_size / 1024.0
            raise forms.ValidationError(_('This image exceeds the max file size'
                                          ' (%sKB)' % formatted_size))
        return f

class LimitedFileTypeField(forms.FileField):

    """
    A form field that will only accept files of certain types. It would be best
    to extend this form and override the valid_extensions and
    valid_content_types

    Bear in mind that this is not 100% safe. It's trivial to alter the mime-type
    and extension of a file, you will still need to verify the file to be
    certain it is of the the desired type
    """

    valid_extensions = ('mp3',)
    valid_content_types = ('audio/mpeg3', 'audio/x-mpeg-3', 'video/mpeg',
                           'video/x-mpeg')

    def __init__(self, valid_extensions=None, valid_content_types=None,
                 *args, **kwargs):
        if valid_extensions:
            self.valid_extensions = valid_extensions
        if valid_content_types:
            self.valid_content_types = valid_content_types
        super(LimitedFileTypeField, self).__init__( *args, **kwargs)

    def clean(self, data, initial=None):
        f = super(LimitedFileTypeField, self).clean(data, initial)
        ext = os.path.splitext(f.name)[1][1:].lower()
        if ext not in self.valid_extensions and \
           data.content_type not in self.valid_content_types:
            raise forms.ValidationError(_('The .%(ext)s file '
                                          'type is not supported' % {'ext': ext}))
        return f

class AuthenticationForm(BaseAuthenticationForm):

    store_login = forms.BooleanField(label=_('Remember me'), required=False)

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
# http://www.djangosnippets.org/snippets/951/

class SubmitButton(forms.Widget):
    """
    A widget that handles a submit button.
    """
    def __init__(self, name, value, label, attrs):
        self.name, self.value, self.label = name, value, label
        self.attrs = attrs

    def __unicode__(self):
        klass = self.attrs.get('class')
        if klass:
            self.attrs['class'] = '%s %s' % (klass, self.value)
        else:
            self.attrs['class'] = self.value
        final_attrs = self.build_attrs(
            self.attrs,
            type="submit",
            name=self.name,
            value=self.value,
            )
        return mark_safe(u'<button%s>%s</button>' % (
            forms.widgets.flatatt(final_attrs),
            self.label,
            ))

class MultipleSubmitButton(forms.Select):
    """
    A widget that handles a list of submit buttons.
    """
    def __init__(self, attrs={}, choices=()):
        self.attrs = attrs
        self.choices = choices

    def __iter__(self):
        for value, label in self.choices:
            yield SubmitButton(self.name, value, label, self.attrs.copy())

    def __unicode__(self):
        return '<button type="submit" />'

    def render(self, name, value, attrs=None, choices=()):
        """Outputs a <ul> for this set of submit buttons."""
        self.name = name
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join(
            [u'<li>%s</li>' % force_unicode(w) for w in self],
            ))
    def value_from_datadict(self, data, files, name):
        """
        returns the value of the widget: IE posts inner HTML of the button
        instead of the value.
        """
        value = data.get(name, None)
        if value in dict(self.choices):
            return value
        else:
            inside_out_choices = dict([(v, k) for (k, v) in self.choices])
            if value in inside_out_choices:
                return inside_out_choices[value]
        return None


class LoginAsForm(forms.Form):
    """
    Sometimes to debug an error you need to login as a specific User.
    This form allows you to log as any user in the system. You can restrict
    the allowed users by passing a User queryset paramter, `qs` when the
    form is instantiated.
    """
    user = forms.ModelChoiceField(User.objects.all())

    def __init__(self, data=None, files=None, request=None, qs=None, *args,
                 **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(LoginAsForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request
        if qs is not None:
            self.fields["user"].queryset = qs


    def save(self):
        user = self.cleaned_data["user"]

        # In lieu of a call to authenticate()
        backend = get_backends()[0]
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        login(self.request, user)

        message = "Logged in as %s" % self.request.user
        self.request.user.message_set.create(message=message)
