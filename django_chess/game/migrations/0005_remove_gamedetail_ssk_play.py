# Generated by Django 5.0.6 on 2024-07-09 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_alter_game_dtm_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedetail',
            name='ssk_play',
        ),
    ]
