from django import forms


class KeywordsForm(forms.Form):
    keywords = forms.CharField(label='keywords', max_length=100)


class UserTextForm(forms.Form):
    text = forms.CharField(label='text', max_length=15000)
