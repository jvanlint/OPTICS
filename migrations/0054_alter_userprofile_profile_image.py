# Generated by Django 3.2.6 on 2021-09-12 07:57

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0053_auto_20210912_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='assets/img/avatars/pilot1.png', force_format='PNG', help_text='User profile image file.', keep_meta=True, quality=0, size=[200, 200], upload_to='user/profile_images/<property object at 0x1039df810>/', verbose_name='User profile image.'),
        ),
    ]