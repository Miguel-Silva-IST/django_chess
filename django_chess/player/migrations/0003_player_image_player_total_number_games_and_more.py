# Generated by Django 5.0.6 on 2024-06-27 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_player_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='player',
            name='total_number_games',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_number_losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_number_wins',
            field=models.IntegerField(default=0),
        ),
    ]
