# Generated by Django 3.1.7 on 2021-04-07 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0002_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='elev',
            field=models.CharField(blank=True, help_text='Enter target elevation.', max_length=200, null=True, verbose_name='Target Elevation'),
        ),
        migrations.AlterField(
            model_name='target',
            name='lat',
            field=models.CharField(blank=True, help_text='Enter target latitude', max_length=200, null=True, verbose_name='Target Latitude'),
        ),
        migrations.AlterField(
            model_name='target',
            name='long',
            field=models.CharField(blank=True, help_text='Enter target longitude.', max_length=200, null=True, verbose_name='Target Longitude'),
        ),
    ]
