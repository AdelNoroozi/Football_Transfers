# Generated by Django 4.1.5 on 2023-03-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats_api', '0008_alter_goal_goal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goaltype',
            name='ratio',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=3),
        ),
    ]
