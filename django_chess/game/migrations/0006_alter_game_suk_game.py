# Generated by Django 5.0.6 on 2024-07-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_remove_gamedetail_ssk_play'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='suk_game',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
