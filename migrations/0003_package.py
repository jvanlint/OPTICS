# Generated by Django 3.1.7 on 2021-03-16 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0002_auto_20210316_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(help_text='Enter Package Name', max_length=20)),
                ('mission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='airops.mission')),
            ],
            options={
                'ordering': ['-package_name'],
            },
        ),
    ]
