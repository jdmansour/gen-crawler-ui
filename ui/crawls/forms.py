""" Forms for the crawls app """
from django import forms

class StartCrawlForm(forms.Form):
    """ Form for starting a new crawl """
    start_url = forms.URLField(label='Start URL', required=True)
    follow_links = forms.BooleanField(label='Follow links', required=False)
