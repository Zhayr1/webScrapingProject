# Generated by Django 4.0 on 2021-12-26 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textSpin', '0004_alter_singlekeywordreport_article_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordsresultsreport',
            name='number_of_keywords',
            field=models.IntegerField(default=0),
        ),
    ]
