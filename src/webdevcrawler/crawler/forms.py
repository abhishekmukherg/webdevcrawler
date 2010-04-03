from django import forms

class CrawlForm(forms.Form):
    url = forms.URLField(verify_exists=True)
