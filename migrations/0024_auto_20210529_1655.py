# Generated by Django 2.2.10 on 2021-05-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0023_auto_20210529_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threatreference',
            name='harm_code',
            field=models.CharField(max_length=25, null=True),
        ),
    ]