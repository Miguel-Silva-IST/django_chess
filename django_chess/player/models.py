from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    suk_player = models.IntegerField(primary_key=True)
    nm_player = models.CharField()
    email_player = models.CharField()
