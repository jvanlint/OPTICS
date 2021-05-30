# Generated by Django 2.2.10 on 2021-05-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0010_support_player_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='aircraft',
            options={'ordering': ['flight_lead']},
        ),
    ]