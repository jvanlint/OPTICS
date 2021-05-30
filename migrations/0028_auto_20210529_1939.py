# Generated by Django 2.2.10 on 2021-05-29 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0027_auto_20210529_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='pilot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_pilot', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='aircraft',
            name='rio_wso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_rio', to=settings.AUTH_USER_MODEL),
        ),
    ]
