# Generated by Django 4.1.5 on 2023-03-13 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0005_alter_playermatchstats_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('ratio', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
        migrations.AddField(
            model_name='goal',
            name='goal_type',
            field=models.ManyToManyField(blank=True, null=True, to='stats_api.goaltype'),
        ),
    ]
