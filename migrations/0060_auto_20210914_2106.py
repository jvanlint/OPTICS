# Generated by Django 3.2.6 on 2021-09-14 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airops', '0059_auto_20210914_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='assets/img/avatars/pilot1.png', force_format='PNG', help_text='User profile image file.', keep_meta=True, quality=0, size=[200, 200], upload_to='user/profile_images/<property object at 0x103d2e8b0>/', verbose_name='User profile image.'),
        ),
    ]
