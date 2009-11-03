from django import forms
from django.core.files import File
from feeds.models import Feed
from feeds.tools import get_favicon

from haystack.forms import SearchForm as HaystackSearchForm

class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('feed_url', 'name')

class EditFeedForm(forms.ModelForm):

    favicon = forms.URLField(required=False)

    class Meta:
        model = Feed
        fields = ('name', 'slug', 'favicon')

    def save(self, commit=True):
        obj = super(EditFeedForm, self).save(commit=False)
        fo = File(open(get_favicon(self.cleaned_data['favicon'])))
        obj.favicon.save(obj.slug+'.ico', fo, save=True)
        return obj


class ReadForm(forms.Form):
    read = forms.BooleanField(widget=forms.HiddenInput)


class SearchForm(HaystackSearchForm):
    pass
