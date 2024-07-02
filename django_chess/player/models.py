from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suk_player = models.IntegerField(primary_key=True)
    username = models.CharField()
    player_name = models.CharField(default='No name defined')
    player_age = models.IntegerField(default=0)
    player_country = models.CharField(default='No country defined')
    player_email = models.CharField()
    player_image = models.ImageField(default='default.png', upload_to = 'profile_pics')
    total_number_games = models.IntegerField(default=0)
    total_number_wins = models.IntegerField(default=0)
    total_number_losses = models.IntegerField(default=0)

