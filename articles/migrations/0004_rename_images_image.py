# Generated by Django 4.1.5 on 2023-03-16 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
