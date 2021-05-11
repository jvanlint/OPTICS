# Generated by Django 2.2.10 on 2021-05-11 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0011_auto_20210511_2233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['task_name']},
        ),
        migrations.AddField(
            model_name='flight',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='airops.Task'),
        ),
    ]