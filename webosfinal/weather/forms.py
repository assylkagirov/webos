from django import forms

class CityForm(forms.Form):
    city = forms.CharField(max_length=255,
    widget=forms.TextInput(attrs={'class':"input", 'type':"text", 'placeholder':"City Name"}))
