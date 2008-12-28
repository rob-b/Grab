from django import forms
from feeds.models import Feed

class FeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('feed_url', 'name')
