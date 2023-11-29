from django import forms

class MyForm(forms.Form):
    old_domain = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Old domain'}))
    new_domain = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New domain'}))
