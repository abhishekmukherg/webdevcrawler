from django import forms

class CrawlForm(forms.Form):
    url = forms.URLField(verify_exists=False)
    limit_to_domain = forms.CharField(max_length=255, required=False)
