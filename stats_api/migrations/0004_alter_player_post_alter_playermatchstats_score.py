# Generated by Django 4.1.5 on 2023-03-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0003_rename_post_playermatchstats_post_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='post',
            field=models.CharField(choices=[('GK', 'GoalKeeper'), ('RB', 'Right Back'), ('CB', 'Center Back'), ('LB', 'Left Back'), ('CDM', 'Center Defensive Midfielder'), ('CM', 'Center Midfielder'), ('RM', 'Right Midfielder'), ('LM', 'Left Midfielder'), ('LW', 'Left Winger'), ('RW', 'Right Winger'), ('ST', 'Striker')], max_length=20),
        ),
        migrations.AlterField(
            model_name='playermatchstats',
            name='score',
            field=models.DecimalField(decimal_places=1, default=5, max_digits=3),
        ),
    ]
