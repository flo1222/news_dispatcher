# Generated by Django 2.1.7 on 2020-12-23 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_dispatcher_app', '0006_site_usual_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='matche_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
