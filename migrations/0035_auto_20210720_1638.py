"""
 Populate the new userProfile table with sensible defaults
 callsign=username
 timezone="Australia/Melbourne"
"""

from django.db import migrations, models


def populate_userprofile(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Profile = apps.get_model("airops", "UserProfile")
    for user in User.objects.all():
        new_profile_record = Profile(
            user=user, timezone="Australia/Melbourne", callsign=user.username
        )
        new_profile_record.save()


class Migration(migrations.Migration):

    dependencies = [
        ("airops", "0034_auto_20210713_1547"),
    ]

    operations = [migrations.RunPython(populate_userprofile)]
