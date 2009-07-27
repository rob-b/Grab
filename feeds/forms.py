from django import forms
from feeds.models import Feed

class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('feed_url', 'name')


class ReadForm(forms.Form):
    read = forms.BooleanField(widget=forms.HiddenInput)
