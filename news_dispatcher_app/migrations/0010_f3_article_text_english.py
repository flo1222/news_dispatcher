# Generated by Django 2.1.7 on 2021-01-02 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_dispatcher_app', '0009_auto_20201231_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='f3_article',
            name='text_english',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
