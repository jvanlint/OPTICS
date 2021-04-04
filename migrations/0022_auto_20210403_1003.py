# Generated by Django 3.1.7 on 2021-04-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0021_auto_20210403_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=models.TextField(default='Campaign description to be added here.', help_text='A brief description used for display purposes on selection screens.'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='description',
            field=models.TextField(default='Mission description to be added here.', help_text='Enter Mission Description/Situation.'),
        ),
    ]
