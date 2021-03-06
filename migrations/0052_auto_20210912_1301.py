# Generated by Django 3.2.6 on 2021-09-12 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airops', '0051_auto_20210912_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='date_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='terrain',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='terrain',
            name='date_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='terrain',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='assets/img/avatars/pilot1.png', force_format='PNG', help_text='User profile image file.', keep_meta=True, quality=0, size=[200, 200], upload_to='user/profile_images/<property object at 0x106892860>/', verbose_name='User profile image.'),
        ),
    ]
