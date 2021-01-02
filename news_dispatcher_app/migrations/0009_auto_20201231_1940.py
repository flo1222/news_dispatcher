# Generated by Django 2.1.7 on 2020-12-31 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_dispatcher_app', '0008_f3_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='f3_article',
            name='is_industrial',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='f3_article',
            name='sorted_industrial',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
