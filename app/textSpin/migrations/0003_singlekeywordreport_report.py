# Generated by Django 4.0 on 2021-12-24 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('textSpin', '0002_alter_singlekeywordreport_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlekeywordreport',
            name='report',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='textSpin.keywordsresultsreport'),
        ),
    ]