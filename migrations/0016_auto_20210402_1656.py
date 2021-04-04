# Generated by Django 3.1.7 on 2021-04-02 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airops', '0015_auto_20210329_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='date',
        ),
        migrations.AddField(
            model_name='campaign',
            name='created_by',
            field=models.CharField(blank=True, help_text='Name of campaign creator.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='situation',
            field=models.TextField(blank=True, help_text='A detailed overview of the background and situation for the campaign.', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='brief',
            field=models.TextField(blank=True, help_text='Enter Detailed Mission Brief.', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_date',
            field=models.DateField(blank=True, help_text='Proposed mission date.', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_time',
            field=models.CharField(blank=True, help_text='Mission time in HH:MM format.', max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='munitions_restrictions',
            field=models.TextField(blank=True, help_text='Enter any restrictions on use of munitions/weaponry.', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='roe',
            field=models.TextField(blank=True, help_text='Enter Rules of Engagement', null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaignImage',
            field=models.ImageField(blank=True, help_text='Campaign Image File.', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='description',
            field=models.TextField(blank=True, help_text='A brief description used for display purposes on selection screens.', null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(help_text='The Campaign Name.', max_length=200),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_date',
            field=models.DateField(blank=True, help_text='Proposed Start Date of Campaign.', null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='number',
            field=models.IntegerField(default=1, help_text='A number representing the mission order within the campaign.'),
        ),
    ]
