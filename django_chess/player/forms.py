from django import forms

class PlayerForm(forms.Form):
    player_name = forms.CharField()
    player_age = forms.IntegerField()
    player_country = forms.CharField()
    player_email = forms.EmailField()
    player_image = forms.ImageField()

