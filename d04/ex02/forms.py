from django import forms

class EntryForm(forms.Form):
    entry = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter text...'}))
