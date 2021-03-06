# Generated by Django 3.2.6 on 2021-08-19 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airops', '0045_merge_20210809_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Squadron',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squadron_name', models.CharField(max_length=50, unique=True, verbose_name='Squadron Name')),
                ('squadron_url', models.URLField(null=True, verbose_name='Squadron Website')),
            ],
            options={
                'db_table': 'user_squadron',
            },
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='callsign',
        ),
        migrations.AlterField(
            model_name='missionfile',
            name='file_type',
            field=models.CharField(choices=[('MIZ', 'Mission'), ('LIB', 'Liberation'), ('COM', 'CombatFlite'), ('OTH', 'Other')], default='MIZ', max_length=10),
        ),
        migrations.AlterField(
            model_name='missionfile',
            name='name',
            field=models.CharField(max_length=100, verbose_name='File Name'),
        ),
        migrations.AlterField(
            model_name='missionfile',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='File Uploader'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='assets/img/avatars/pilot1.png', force_format='PNG', help_text='User profile image file.', keep_meta=True, quality=0, size=[200, 200], upload_to='user/profile_images/<property object at 0x0000022EFFB4C7C0>/', verbose_name='User profile image.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default='Australia/Melbourne', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='squadron',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='airops.squadron', verbose_name='Squadron'),
        ),
    ]
