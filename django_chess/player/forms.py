from django.forms import ModelForm
from player.models import Player

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['player_name', 'player_age', 'player_country', 'player_email','player_image']

