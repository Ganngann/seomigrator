from django import forms
from django.core.exceptions import ValidationError

class MyForm(forms.Form):
    old_domain = forms.CharField(
        label="Old Domain",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "https://example.com"}
        )
    )
    new_domain = forms.CharField(
        label="New Domain",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "https://dev.example.com"}
        )
    )
    new_url_to_index = forms.IntegerField(
        label="New URLs to add to the index of new urls",
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "class": "form-range",
                "id": "new_urls_to_index",
                "min": 0,
                "max": 250,
                "oninput": "updateValue(this.value)",
                "value": 0,
            }
        )
    )

    def clean_old_domain(self):
        old_domain = self.cleaned_data.get('old_domain')
        if not old_domain.startswith('http'):
            raise forms.ValidationError('Domain must start with "http".')
        return old_domain

    def clean_new_domain(self):
        new_domain = self.cleaned_data.get('new_domain')
        if not new_domain.startswith('http'):
            raise forms.ValidationError('Domain must start with "http".')
        return new_domain
