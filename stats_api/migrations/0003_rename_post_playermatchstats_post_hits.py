# Generated by Django 4.1.5 on 2023-03-09 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0002_playermatchstats_chances_missed_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playermatchstats',
            old_name='post',
            new_name='post_hits',
        ),
    ]