# Generated by Django 4.1.5 on 2023-03-16 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0011_alter_goal_goal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamtournamentstats',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_tournament_stats', to='stats_api.team'),
        ),
        migrations.AlterField(
            model_name='teamtournamentstats',
            name='tournament_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_tournament_stats', to='stats_api.tournamentseason'),
        ),
    ]
