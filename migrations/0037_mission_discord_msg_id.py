# Generated by Django 3.2.4 on 2021-07-22 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0036_auto_20210722_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='discord_msg_id',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Discord Msg ID'),
        ),
    ]
