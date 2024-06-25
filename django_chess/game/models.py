from django.db import models
from django.contrib.postgres.fields import ArrayField
from player.models import Player

class Game(models.Model):
    suk_game = models.IntegerField(primary_key=True)
    dtm_game = models.DateField()

class GameDetail(models.Model):
    suk_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ssk_play = models.IntegerField()
    suk_player = models.ForeignKey(Player, on_delete=models.CASCADE)
    board_state = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=8,
        ),
        size=8,
    )


