from django import forms

class Upload_Image(forms.Form):
    image = forms.ImageField()

