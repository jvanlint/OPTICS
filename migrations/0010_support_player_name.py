# Generated by Django 2.2.10 on 2021-05-09 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0009_auto_20210425_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='player_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]