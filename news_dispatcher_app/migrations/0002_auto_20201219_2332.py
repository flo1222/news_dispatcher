# Generated by Django 2.1.7 on 2020-12-19 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_dispatcher_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articles',
            new_name='Article',
        ),
    ]
