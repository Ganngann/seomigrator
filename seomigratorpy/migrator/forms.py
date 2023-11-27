from django import forms

class MyForm(forms.Form):
    old_domain = forms.CharField(widget=forms.TextInput(attrs={'id': 'old_domain'}))
    new_domain = forms.CharField(widget=forms.TextInput(attrs={'id': 'new_domain'}))
