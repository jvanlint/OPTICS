# Generated by Django 3.2.6 on 2021-09-15 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0066_populate_type_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support',
            name='temp_type',
        ),
        migrations.RemoveField(
            model_name='threat',
            name='temp_type',
        ),
        migrations.RemoveField(
            model_name='waypoint',
            name='temp_type',
        ),
    ]