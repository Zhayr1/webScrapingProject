# Generated by Django 4.0 on 2021-12-24 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textSpin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlekeywordreport',
            name='article_title',
            field=models.TextField(),
        ),
    ]
