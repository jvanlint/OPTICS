# Generated by Django 3.1.7 on 2021-03-16 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter Operation Name', max_length=20)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
    ]
