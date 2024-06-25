from django.db import models

class Player(models.Model):
    suk_player = models.IntegerField(primary_key=True)
    nm_player = models.CharField()
    email_player = models.CharField()
