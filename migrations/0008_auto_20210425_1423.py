# Generated by Django 2.2.10 on 2021-04-25 04:23

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0007_auto_20210425_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='aoImage',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', help_text='An image of the Area of Operations.', keep_meta=True, null=True, quality=0, size=[1500, 1200], upload_to='campaign/ao_images', verbose_name='area of Operations Image'),
        ),
    ]
