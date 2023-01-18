from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'search_input',
                                                                   'placeholder': "Search"}))
