from django.db import models
from django.contrib.postgres.fields import ArrayField
from player.models import Player
import datetime

class Game(models.Model):
    suk_game = models.IntegerField(primary_key=True)
    suk_player_1 = models.ForeignKey(Player,related_name='games_as_player_1', on_delete=models.CASCADE) 
    suk_player_2 = models.ForeignKey(Player, related_name='games_as_player_2', on_delete=models.CASCADE)
    game_active = models.BooleanField(default=False)
    dtm_game = models.DateField(default=datetime.date.today)

class GameDetail(models.Model):
    suk_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    suk_player = models.ForeignKey(Player, on_delete=models.CASCADE)
    board_state = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=8,
        ),
        size=8,
    )


