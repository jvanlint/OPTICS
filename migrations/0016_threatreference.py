# Generated by Django 2.2.10 on 2021-05-29 03:28

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0015_remove_campaign_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreatReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('nato_code', models.CharField(max_length=60)),
                ('threat_class', models.CharField(choices=[('AAA', 'AAA'), ('MANPAD', 'MANPAD'), ('SHORAD', 'SHORAD'), ('MEDRAD', 'MEDRAD'), ('LONRAD', 'LONRAD'), ('TGTRDR', 'TGTRDR'), ('EWR-ACQR', 'EWR-ACQR')], max_length=10, null=True)),
                ('rwr_image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', help_text='Upload image for rwr.', keep_meta=True, null=True, quality=0, size=[1500, 1200], upload_to='threats', verbose_name='RWR Identifier')),
                ('description', models.TextField(default='Threat description to be added here.', help_text='Enter Threat Description/Situation.')),
            ],
        ),
    ]
