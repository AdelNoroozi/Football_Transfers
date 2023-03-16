# Generated by Django 4.1.5 on 2023-03-15 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0009_alter_goaltype_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamTournamentStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('loses', models.PositiveIntegerField(default=0)),
                ('draws', models.PositiveIntegerField(default=0)),
                ('goals_scored', models.PositiveIntegerField(default=0)),
                ('goals_received', models.PositiveIntegerField(default=0)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='stats_api.team')),
                ('tournament_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='stats_api.tournamentseason')),
            ],
        ),
    ]