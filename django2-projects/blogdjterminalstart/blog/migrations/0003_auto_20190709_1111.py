# Generated by Django 2.2.3 on 2019-07-09 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190709_0818'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='tag',
            new_name='slug',
        ),
    ]