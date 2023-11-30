from django import forms

class MyForm(forms.Form):
    old_domain = forms.CharField(
        label="Old Domain",  # Ajout du label ici
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Old domain"}
        )
    )
    new_domain = forms.CharField(
        label="New Domain",  # Ajout du label ici
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "New domain"}
        )
    )
    new_url_to_index = forms.IntegerField(
        label="New URLs to add to the index",  # Ajout du label ici
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "class": "form-range",
                "id": "new_urls_to_index",
                "min": 0,
                "max": 100,
                "oninput": "updateValue(this.value)",
                "value": 50,
            }
        )
    )
