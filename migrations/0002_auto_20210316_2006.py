# Generated by Django 3.1.7 on 2021-03-16 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(help_text='Enter Operation Name', max_length=200)),
                ('start_date', models.DateTimeField()),
                ('status', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['-campaign_name'],
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission_name', models.CharField(help_text='Enter Mission Name', max_length=20)),
                ('mission_date', models.DateTimeField()),
                ('campaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='airops.campaign')),
            ],
            options={
                'ordering': ['-mission_name'],
            },
        ),
        migrations.DeleteModel(
            name='Operation',
        ),
    ]
