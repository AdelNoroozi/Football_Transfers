# Generated by Django 4.1.5 on 2023-01-28 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_player_age_alter_popularities_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='market_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True),
        ),
    ]