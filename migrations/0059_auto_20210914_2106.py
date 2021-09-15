# Generated by Django 3.2.6 on 2021-09-14 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airops', '0058_auto_20210914_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='creator',
        ),
        migrations.AddField(
            model_name='campaign',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaign_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaign_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='assets/img/avatars/pilot1.png', force_format='PNG', help_text='User profile image file.', keep_meta=True, quality=0, size=[200, 200], upload_to='user/profile_images/<property object at 0x10660f7c0>/', verbose_name='User profile image.'),
        ),
    ]