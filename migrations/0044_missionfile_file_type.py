# Generated by Django 3.2.4 on 2021-08-07 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0043_auto_20210801_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='missionfile',
            name='file_type',
            field=models.CharField(choices=[('MIZ', 'MIZ'), ('LIB', 'Liberation'), ('COM', 'CombatFlite')], default='MIZ', max_length=10),
        ),
    ]
