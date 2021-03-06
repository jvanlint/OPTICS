# Generated by Django 2.2.10 on 2021-05-29 06:41

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0021_threatreference_harm_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='threatreference',
            name='rwr_image2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', help_text='Upload image for rwr.', keep_meta=True, null=True, quality=0, size=[1920, 1080], upload_to='threats', verbose_name='RWR Identifier'),
        ),
        migrations.AddField(
            model_name='threatreference',
            name='rwr_image3',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', help_text='Upload image for rwr.', keep_meta=True, null=True, quality=0, size=[1920, 1080], upload_to='threats', verbose_name='RWR Identifier'),
        ),
        migrations.AlterField(
            model_name='threatreference',
            name='rwr_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', help_text='Upload image for rwr.', keep_meta=True, null=True, quality=0, size=[1920, 1080], upload_to='threats', verbose_name='RWR Identifier'),
        ),
    ]
