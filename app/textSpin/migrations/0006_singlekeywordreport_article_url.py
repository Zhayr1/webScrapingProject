# Generated by Django 4.0 on 2021-12-26 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textSpin', '0005_keywordsresultsreport_number_of_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlekeywordreport',
            name='article_url',
            field=models.CharField(default=0, max_length=409, null=True),
        ),
    ]
